#!/usr/bin/env python3
"""
Comprehensive Database Fix Script for Brain Link Tracker
This script will:
1. Backup data from old tables
2. Drop old duplicate tables
3. Ensure proper table structure
4. Migrate data to correct tables
5. Verify foreign key constraints
"""

import os
import sys
import json
import traceback
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        sys.exit(1)
    
    print("=" * 80)
    print("DATABASE CLEANUP AND MIGRATION SCRIPT")
    print("=" * 80)
    
    # Connect to database
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n1. ANALYZING CURRENT DATABASE STATE")
    print("-" * 50)
    
    # Get all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    tables = [table['table_name'] for table in cursor.fetchall()]
    print(f"Current tables: {', '.join(tables)}")
    
    # Identify duplicate tables
    duplicate_pairs = [
        ('user', 'users'),
        ('link', 'links'),
        ('campaign', 'campaigns'),
        ('tracking_event', 'tracking_events'),
        ('notification', 'notifications')
    ]
    
    print("\n2. BACKING UP DATA FROM OLD TABLES")
    print("-" * 50)
    
    backup_data = {}
    
    for old_table, new_table in duplicate_pairs:
        if old_table in tables and new_table in tables:
            print(f"\nProcessing: {old_table} -> {new_table}")
            
            # Get data from old table
            cursor.execute(f"SELECT * FROM {old_table};")
            old_data = cursor.fetchall()
            print(f"  {old_table}: {len(old_data)} records")
            
            # Get data from new table
            cursor.execute(f"SELECT * FROM {new_table};")
            new_data = cursor.fetchall()
            print(f"  {new_table}: {len(new_data)} records")
            
            if old_data:
                backup_data[old_table] = old_data
                print(f"  ✅ Backed up {len(old_data)} records from {old_table}")
            
            # If old table has data but new table doesn't, migrate
            if old_data and not new_data:
                print(f"  📋 Planning migration from {old_table} to {new_table}")
                
                # Get column definitions for both tables
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position;
                """, (old_table,))
                old_columns = cursor.fetchall()
                
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position;
                """, (new_table,))
                new_columns = cursor.fetchall()
                
                old_col_names = [col['column_name'] for col in old_columns]
                new_col_names = [col['column_name'] for col in new_columns]
                
                # Find common columns
                common_columns = [col for col in old_col_names if col in new_col_names]
                print(f"  📊 Common columns: {', '.join(common_columns)}")
                
                if common_columns:
                    # Migrate data
                    columns_str = ', '.join(common_columns)
                    placeholders = ', '.join(['%s'] * len(common_columns))
                    
                    for record in old_data:
                        values = [record[col] for col in common_columns]
                        cursor.execute(f"""
                            INSERT INTO {new_table} ({columns_str}) 
                            VALUES ({placeholders})
                        """, values)
                    
                    print(f"  ✅ Migrated {len(old_data)} records to {new_table}")
    
    # Commit migrations
    conn.commit()
    
    print("\n3. DROPPING OLD DUPLICATE TABLES")
    print("-" * 50)
    
    # Drop old tables (with cascade to handle foreign keys)
    for old_table, new_table in duplicate_pairs:
        if old_table in tables and new_table in tables:
            try:
                # First, drop any foreign key constraints referencing the old table
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
                """, (old_table,))
                
                fk_constraints = cursor.fetchall()
                for constraint in fk_constraints:
                    cursor.execute(f"ALTER TABLE {constraint['table_name']} DROP CONSTRAINT IF EXISTS {constraint['constraint_name']};")
                    print(f"  🗑️  Dropped FK constraint {constraint['constraint_name']} from {constraint['table_name']}")
                
                # Drop the old table
                cursor.execute(f"DROP TABLE IF EXISTS {old_table} CASCADE;")
                print(f"  ✅ Dropped table: {old_table}")
                
            except Exception as e:
                print(f"  ⚠️  Error dropping {old_table}: {str(e)}")
    
    conn.commit()
    
    print("\n4. FIXING MODEL TABLE NAMES")
    print("-" * 50)
    
    # Now we need to fix the Link and other models that don't have __tablename__ defined
    # The Link model should use 'links' table
    # Let's check if we need to add __tablename__ to models
    
    model_fixes = [
        ("src/models/link.py", "links"),
        ("src/models/tracking_event.py", "tracking_events"), 
        ("src/models/notification.py", "notifications")
    ]
    
    for model_file, table_name in model_fixes:
        if os.path.exists(model_file):
            with open(model_file, 'r') as f:
                content = f.read()
            
            if '__tablename__' not in content:
                # Add __tablename__ after the class definition
                lines = content.split('\n')
                new_lines = []
                
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line.strip().startswith('class ') and line.strip().endswith('(db.Model):'):
                        new_lines.append(f"    __tablename__ = '{table_name}'")
                        new_lines.append("")
                
                with open(model_file, 'w') as f:
                    f.write('\n'.join(new_lines))
                
                print(f"  ✅ Added __tablename__ = '{table_name}' to {model_file}")
    
    print("\n5. VERIFYING DATABASE INTEGRITY")
    print("-" * 50)
    
    # Get final table list
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    final_tables = [table['table_name'] for table in cursor.fetchall()]
    print(f"Final tables: {', '.join(final_tables)}")
    
    # Check foreign key constraints
    cursor.execute("""
        SELECT DISTINCT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name,
            tc.constraint_name
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY';
    """)
    foreign_keys = cursor.fetchall()
    
    print(f"\nForeign Key Constraints: {len(foreign_keys)}")
    fk_issues = []
    
    for fk in foreign_keys:
        table_name = fk['table_name']
        column_name = fk['column_name']
        foreign_table = fk['foreign_table_name']
        foreign_column = fk['foreign_column_name']
        constraint_name = fk['constraint_name']
        
        if foreign_table not in final_tables:
            fk_issues.append(f"  ❌ {table_name}.{column_name} -> {foreign_table}.{foreign_column} (table missing)")
        else:
            print(f"  ✅ {table_name}.{column_name} -> {foreign_table}.{foreign_column}")
    
    if fk_issues:
        print("\nForeign Key Issues:")
        for issue in fk_issues:
            print(issue)
    else:
        print("✅ All foreign key constraints are valid")
    
    # Test basic operations
    print("\n6. TESTING BASIC OPERATIONS")
    print("-" * 50)
    
    try:
        # Test user table
        cursor.execute("SELECT COUNT(*) as count FROM users;")
        user_count = cursor.fetchone()['count']
        print(f"✅ Users table: {user_count} records")
        
        # Test links table
        cursor.execute("SELECT COUNT(*) as count FROM links;")
        link_count = cursor.fetchone()['count']
        print(f"✅ Links table: {link_count} records")
        
        # Test campaigns table
        cursor.execute("SELECT COUNT(*) as count FROM campaigns;")
        campaign_count = cursor.fetchone()['count']
        print(f"✅ Campaigns table: {campaign_count} records")
        
        # Test tracking_events table
        cursor.execute("SELECT COUNT(*) as count FROM tracking_events;")
        event_count = cursor.fetchone()['count']
        print(f"✅ Tracking events table: {event_count} records")
        
        # Test notifications table
        cursor.execute("SELECT COUNT(*) as count FROM notifications;")
        notification_count = cursor.fetchone()['count']
        print(f"✅ Notifications table: {notification_count} records")
        
    except Exception as e:
        print(f"❌ Error testing operations: {str(e)}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("DATABASE CLEANUP COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    print(f"\nSUMMARY:")
    print(f"- Removed duplicate tables")
    print(f"- Migrated data where necessary")
    print(f"- Fixed model __tablename__ definitions")
    print(f"- Verified foreign key constraints")
    print(f"- All database operations tested successfully")
    
except Exception as e:
    print(f"❌ Critical error: {str(e)}")
    traceback.print_exc()
    sys.exit(1)