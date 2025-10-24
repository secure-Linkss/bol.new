#!/usr/bin/env python3
"""
COMPREHENSIVE PROJECT AUDIT AND FIX SCRIPT
==========================================
This script will:
1. Connect to the production database
2. Verify all tables and columns exist
3. Check the "Brain" admin account and its tracking links
4. Verify all models are properly synced
5. Fix any missing database schema elements
6. Generate a detailed report
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Database connection string
# Parse from environment variable format
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-a4e4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')

def connect_db():
    """Connect to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def get_all_tables(conn):
    """Get list of all tables in the database"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return tables

def get_table_columns(conn, table_name):
    """Get all columns for a specific table"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    columns = cursor.fetchall()
    cursor.close()
    return columns

def check_brain_account(conn):
    """Check the Brain admin account and its data"""
    cursor = conn.cursor()
    
    # Get Brain user details
    cursor.execute("""
        SELECT id, username, email, role, status, plan_type, created_at, last_login, login_count
        FROM users
        WHERE username = 'Brain' OR email LIKE '%brain%'
        ORDER BY created_at
        LIMIT 5;
    """)
    users = cursor.fetchall()
    
    print("\n" + "="*80)
    print("🔍 BRAIN ADMIN ACCOUNT AUDIT")
    print("="*80)
    
    if not users:
        print("❌ No 'Brain' admin account found!")
        cursor.close()
        return None
    
    for user in users:
        user_id, username, email, role, status, plan_type, created_at, last_login, login_count = user
        print(f"\n✅ Found User: {username} (ID: {user_id})")
        print(f"   Email: {email}")
        print(f"   Role: {role}")
        print(f"   Status: {status}")
        print(f"   Plan: {plan_type}")
        print(f"   Created: {created_at}")
        print(f"   Last Login: {last_login}")
        print(f"   Login Count: {login_count}")
        
        # Check tracking links for this user
        cursor.execute("""
            SELECT COUNT(*), 
                   COUNT(DISTINCT campaign_name) as unique_campaigns
            FROM links
            WHERE user_id = %s;
        """, (user_id,))
        link_stats = cursor.fetchone()
        
        print(f"\n   📊 Tracking Links Statistics:")
        print(f"      Total Links: {link_stats[0]}")
        print(f"      Unique Campaigns: {link_stats[1]}")
        
        # Get campaign details
        cursor.execute("""
            SELECT campaign_name, COUNT(*) as link_count
            FROM links
            WHERE user_id = %s AND campaign_name IS NOT NULL
            GROUP BY campaign_name
            ORDER BY link_count DESC;
        """, (user_id,))
        campaigns = cursor.fetchall()
        
        if campaigns:
            print(f"\n   📁 Campaigns:")
            for camp_name, link_count in campaigns:
                print(f"      • {camp_name}: {link_count} link(s)")
        
        # Check tracking events
        cursor.execute("""
            SELECT COUNT(*) as total_events,
                   COUNT(DISTINCT ip_address) as unique_visitors,
                   COUNT(CASE WHEN captured_email IS NOT NULL THEN 1 END) as email_captures
            FROM tracking_events te
            JOIN links l ON te.link_id = l.id
            WHERE l.user_id = %s;
        """, (user_id,))
        event_stats = cursor.fetchone()
        
        print(f"\n   📈 Tracking Events:")
        print(f"      Total Events: {event_stats[0]}")
        print(f"      Unique Visitors: {event_stats[1]}")
        print(f"      Email Captures: {event_stats[2]}")
    
    cursor.close()
    return users[0][0]  # Return the first user ID

def verify_required_tables(conn):
    """Verify all required tables exist"""
    required_tables = [
        'users',
        'links',
        'campaigns',
        'tracking_events',
        'notifications',
        'security_threats',
        'audit_logs',
        'support_tickets',
        'subscription_verifications',
        'admin_settings',
        'domains'
    ]
    
    existing_tables = get_all_tables(conn)
    
    print("\n" + "="*80)
    print("🔍 DATABASE TABLE VERIFICATION")
    print("="*80)
    
    missing_tables = []
    for table in required_tables:
        if table in existing_tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' MISSING")
            missing_tables.append(table)
    
    return missing_tables

def verify_user_table_columns(conn):
    """Verify users table has all required columns"""
    required_columns = {
        'id', 'username', 'email', 'password_hash', 'role', 'status',
        'last_login', 'last_ip', 'login_count', 'failed_login_attempts',
        'is_active', 'is_verified', 'plan_type', 'subscription_expiry',
        'created_at', 'updated_at', 'avatar', 'profile_picture',
        'telegram_bot_token', 'telegram_chat_id', 'telegram_enabled',
        'subscription_plan', 'subscription_status', 'subscription_end_date'
    }
    
    columns = get_table_columns(conn, 'users')
    existing_columns = {col[0] for col in columns}
    
    print("\n" + "="*80)
    print("🔍 USERS TABLE COLUMN VERIFICATION")
    print("="*80)
    
    missing_columns = required_columns - existing_columns
    
    for col in required_columns:
        if col in existing_columns:
            print(f"✅ Column '{col}' exists")
        else:
            print(f"❌ Column '{col}' MISSING")
    
    return missing_columns

def create_missing_columns(conn):
    """Create any missing columns in the users table"""
    cursor = conn.cursor()
    
    # Define columns that might be missing with their SQL definitions
    potential_missing_columns = {
        'avatar': "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar VARCHAR(500);",
        'profile_picture': "ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(500);",
        'telegram_bot_token': "ALTER TABLE users ADD COLUMN IF NOT EXISTS telegram_bot_token VARCHAR(255);",
        'telegram_chat_id': "ALTER TABLE users ADD COLUMN IF NOT EXISTS telegram_chat_id VARCHAR(100);",
        'telegram_enabled': "ALTER TABLE users ADD COLUMN IF NOT EXISTS telegram_enabled BOOLEAN DEFAULT FALSE;",
        'subscription_plan': "ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_plan VARCHAR(50);",
        'subscription_status': "ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(50) DEFAULT 'active';",
        'subscription_end_date': "ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_end_date TIMESTAMP;",
        'reset_token': "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255);",
        'reset_token_expiry': "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expiry TIMESTAMP;",
        'account_locked_until': "ALTER TABLE users ADD COLUMN IF NOT EXISTS account_locked_until TIMESTAMP;",
        'settings': "ALTER TABLE users ADD COLUMN IF NOT EXISTS settings TEXT;",
        'notification_settings': "ALTER TABLE users ADD COLUMN IF NOT EXISTS notification_settings TEXT;",
        'preferences': "ALTER TABLE users ADD COLUMN IF NOT EXISTS preferences TEXT;",
        'user_metadata': "ALTER TABLE users ADD COLUMN IF NOT EXISTS user_metadata TEXT;",
    }
    
    print("\n" + "="*80)
    print("🔧 CREATING MISSING COLUMNS")
    print("="*80)
    
    for col_name, sql_statement in potential_missing_columns.items():
        try:
            cursor.execute(sql_statement)
            conn.commit()
            print(f"✅ Ensured column '{col_name}' exists")
        except Exception as e:
            print(f"⚠️  Column '{col_name}': {str(e)[:100]}")
            conn.rollback()
    
    cursor.close()

def verify_links_table_columns(conn):
    """Verify links table has campaign_name column"""
    columns = get_table_columns(conn, 'links')
    existing_columns = {col[0] for col in columns}
    
    print("\n" + "="*80)
    print("🔍 LINKS TABLE COLUMN VERIFICATION")
    print("="*80)
    
    required_cols = ['campaign_name', 'status', 'is_active', 'short_code', 'target_url', 'user_id']
    
    for col in required_cols:
        if col in existing_columns:
            print(f"✅ Column '{col}' exists")
        else:
            print(f"❌ Column '{col}' MISSING")
    
    return required_cols, existing_columns

def check_campaign_data_consistency(conn, user_id):
    """Check if campaigns in Campaign table match campaign_name in Links table"""
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("🔍 CAMPAIGN DATA CONSISTENCY CHECK")
    print("="*80)
    
    # Get distinct campaign names from links table
    cursor.execute("""
        SELECT DISTINCT campaign_name, COUNT(*) as link_count
        FROM links
        WHERE user_id = %s AND campaign_name IS NOT NULL AND campaign_name != ''
        GROUP BY campaign_name;
    """, (user_id,))
    link_campaigns = cursor.fetchall()
    
    print(f"\n📊 Campaign names found in Links table:")
    for camp_name, count in link_campaigns:
        print(f"   • {camp_name}: {count} link(s)")
    
    # Get campaigns from campaigns table
    cursor.execute("""
        SELECT name, id, status
        FROM campaigns
        WHERE owner_id = %s;
    """, (user_id,))
    campaign_table_entries = cursor.fetchall()
    
    print(f"\n📊 Campaigns in Campaigns table:")
    if campaign_table_entries:
        for camp_name, camp_id, status in campaign_table_entries:
            print(f"   • {camp_name} (ID: {camp_id}, Status: {status})")
    else:
        print("   ⚠️  No campaigns found in campaigns table!")
    
    # Check for mismatches
    link_campaign_names = {camp[0] for camp in link_campaigns}
    table_campaign_names = {camp[0] for camp in campaign_table_entries}
    
    missing_in_table = link_campaign_names - table_campaign_names
    
    if missing_in_table:
        print(f"\n⚠️  Campaigns in Links but NOT in Campaigns table:")
        for name in missing_in_table:
            print(f"   • {name}")
            # Auto-create missing campaigns
            try:
                cursor.execute("""
                    INSERT INTO campaigns (name, description, owner_id, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (name, 'Auto-created from existing links', user_id, 'active', datetime.utcnow(), datetime.utcnow()))
                conn.commit()
                print(f"      ✅ Auto-created campaign '{name}'")
            except Exception as e:
                print(f"      ❌ Failed to create: {e}")
                conn.rollback()
    else:
        print("\n✅ All link campaigns exist in campaigns table!")
    
    cursor.close()

def generate_report(conn):
    """Generate a comprehensive report"""
    print("\n" + "="*80)
    print("📋 COMPREHENSIVE PROJECT AUDIT REPORT")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tables = get_all_tables(conn)
    print(f"\n✅ Total Tables: {len(tables)}")
    print(f"   Tables: {', '.join(tables)}")
    
    cursor = conn.cursor()
    
    # Count records in key tables
    key_tables = ['users', 'links', 'campaigns', 'tracking_events']
    print(f"\n📊 Record Counts:")
    for table in key_tables:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"   • {table}: {count} records")
    
    cursor.close()

def main():
    print("="*80)
    print("🚀 COMPREHENSIVE PROJECT AUDIT AND FIX")
    print("="*80)
    print("This script will audit and fix your marketing tracker project")
    print("="*80)
    
    # Connect to database
    conn = connect_db()
    if not conn:
        sys.exit(1)
    
    try:
        # 1. Verify tables
        missing_tables = verify_required_tables(conn)
        
        # 2. Verify user table columns
        missing_user_cols = verify_user_table_columns(conn)
        
        # 3. Create missing columns
        if missing_user_cols:
            create_missing_columns(conn)
        
        # 4. Verify links table
        verify_links_table_columns(conn)
        
        # 5. Check Brain account
        brain_user_id = check_brain_account(conn)
        
        # 6. Check campaign data consistency
        if brain_user_id:
            check_campaign_data_consistency(conn, brain_user_id)
        
        # 7. Generate report
        generate_report(conn)
        
        print("\n" + "="*80)
        print("✅ AUDIT COMPLETE!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error during audit: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
