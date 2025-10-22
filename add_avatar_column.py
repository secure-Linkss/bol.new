#!/usr/bin/env python3
"""
Add avatar_url column to users table
"""
import os
import psycopg2
from psycopg2 import sql

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require')

def add_avatar_column():
    """Add avatar_url column to users table if it doesn't exist"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='avatar_url';
        """)
        
        if cursor.fetchone() is None:
            print("Adding avatar_url column to users table...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN avatar_url VARCHAR(500);
            """)
            conn.commit()
            print("✓ avatar_url column added successfully")
        else:
            print("✓ avatar_url column already exists")
        
        cursor.close()
        conn.close()
        print("\n✓ Database migration completed successfully")
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        raise

if __name__ == "__main__":
    add_avatar_column()
