import psycopg2
import sys

DATABASE_URL = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require'

REQUIRED_TABLES = [
    'users', 'campaigns', 'links', 'domains', 'notifications',
    'api_usage', 'audit_logs', 'payment_methods', 'subscription_history',
    'security_settings', 'support_tickets', 'support_ticket_comments',
    'system_metrics', 'tracking_events', 'link_analytics',
    'blocked_ips', 'blocked_countries', 'security_threats'
]

def verify_schema():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Get all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        existing_tables = [row[0] for row in cur.fetchall()]
        
        print("=" * 60)
        print("DATABASE SCHEMA VERIFICATION REPORT")
        print("=" * 60)
        print(f"\n✅ Total tables found: {len(existing_tables)}")
        print("\n📋 Existing tables:")
        for table in sorted(existing_tables):
            print(f"  ✓ {table}")
        
        # Check for required tables
        missing_tables = [t for t in REQUIRED_TABLES if t not in existing_tables]
        
        print(f"\n{'=' * 60}")
        print("REQUIRED TABLES CHECK")
        print("=" * 60)
        
        if missing_tables:
            print(f"\n⚠️  Missing {len(missing_tables)} required tables:")
            for table in missing_tables:
                print(f"  ✗ {table}")
            print("\n❌ Schema incomplete - missing tables found!")
            return False
        else:
            print("\n✅ All required tables present!")
            
        # Get row counts for key tables
        print(f"\n{'=' * 60}")
        print("TABLE ROW COUNTS")
        print("=" * 60)
        for table in ['users', 'campaigns', 'links']:
            if table in existing_tables:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"  {table}: {count} rows")
        
        cur.close()
        conn.close()
        
        print(f"\n{'=' * 60}")
        print("✅ DATABASE SCHEMA VERIFICATION COMPLETE")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Database verification error: {e}")
        return False

if __name__ == "__main__":
    success = verify_schema()
    sys.exit(0 if success else 1)
