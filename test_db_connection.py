#!/usr/bin/env python3
import os
import sys
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import psycopg2
    from urllib.parse import urlparse
    
    database_url = os.environ.get('DATABASE_URL')
    print(f"Database URL configured: {database_url is not None}")
    
    if database_url:
        # Parse the database URL
        parsed = urlparse(database_url)
        print(f"Database host: {parsed.hostname}")
        print(f"Database name: {parsed.path[1:]}")  # Remove leading slash
        print(f"Database user: {parsed.username}")
        
        # Test connection
        print("\nTesting database connection...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\nExisting tables ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check table schemas
        if tables:
            print("\nTable schemas:")
            for table in tables:
                table_name = table[0]
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position;
                """, (table_name,))
                columns = cursor.fetchall()
                print(f"\n  Table: {table_name}")
                for col in columns:
                    print(f"    - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'} {f'DEFAULT {col[3]}' if col[3] else ''}")
        
        # Check foreign key constraints
        cursor.execute("""
            SELECT 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
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
        print(f"\nForeign key constraints ({len(foreign_keys)}):")
        for fk in foreign_keys:
            print(f"  - {fk[0]}.{fk[1]} -> {fk[2]}.{fk[3]}")
        
        cursor.close()
        conn.close()
        print("\n✅ Database connection successful!")
        
    else:
        print("❌ No DATABASE_URL found in environment variables")
        
except Exception as e:
    print(f"❌ Database connection failed: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    traceback.print_exc()