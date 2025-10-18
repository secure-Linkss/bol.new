#!/usr/bin/env python3
"""
Fix PostgreSQL reserved keyword issues
"""

import os
import sys
import traceback
from dotenv import load_dotenv

load_dotenv()

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    database_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    conn.autocommit = True  # Enable autocommit to avoid transaction issues
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print("FIXING RESERVED KEYWORD ISSUES")
    print("=" * 50)
    
    # Drop tables with reserved keywords using quotes
    reserved_tables = ['user', 'link', 'campaign', 'tracking_event', 'notification']
    
    for table in reserved_tables:
        try:
            print(f"Attempting to drop table: {table}")
            
            # First check if table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (table,))
            
            exists = cursor.fetchone()['exists']
            
            if exists:
                # Drop foreign key constraints first
                cursor.execute("""
                    SELECT 
                        tc.constraint_name,
                        tc.table_name
                    FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                          ON tc.constraint_name = kcu.constraint_name
                          AND tc.table_schema = kcu.table_schema
                        JOIN information_schema.constraint_column_usage AS ccu
                          ON ccu.constraint_name = tc.constraint_name
                          AND ccu.table_schema = tc.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY' 
                    AND ccu.table_name = %s;
                """, (table,))
                
                fk_constraints = cursor.fetchall()
                
                for constraint in fk_constraints:
                    cursor.execute(f'ALTER TABLE "{constraint["table_name"]}" DROP CONSTRAINT IF EXISTS "{constraint["constraint_name"]}";')
                    print(f"  🗑️  Dropped FK constraint {constraint['constraint_name']}")
                
                # Drop the table using quotes to handle reserved keywords
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                print(f"  ✅ Successfully dropped table: {table}")
            else:
                print(f"  ℹ️  Table {table} does not exist")
                
        except Exception as e:
            print(f"  ❌ Error dropping {table}: {str(e)}")
    
    # Verify final state
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    final_tables = [table['table_name'] for table in cursor.fetchall()]
    print(f"\nFinal tables: {', '.join(final_tables)}")
    
    # Check for any remaining duplicate issues
    duplicates_found = False
    for old_table in reserved_tables:
        if old_table in final_tables:
            new_table = old_table + 's'  # users, links, campaigns, etc.
            if new_table in final_tables:
                print(f"⚠️  Still have both {old_table} and {new_table}")
                duplicates_found = True
    
    if not duplicates_found:
        print("✅ No more duplicate table issues!")
    
    cursor.close()
    conn.close()
    
    print("\nReserved keyword fixes completed!")
    
except Exception as e:
    print(f"❌ Critical error: {str(e)}")
    traceback.print_exc()
    sys.exit(1)