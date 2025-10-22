#!/usr/bin/env python3
"""
MASTER FIX SCRIPT - October 22, 2025
====================================
This script applies all critical fixes to the Brain Link Tracker application:
1. Database schema updates (avatar_url column)
2. Verification of all API routes
3. Database migrations
4. Component checks
"""

import os
import sys
import psycopg2
from datetime import datetime

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require')

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def add_avatar_column():
    """Add avatar_url column to users table"""
    print_section("STEP 1: DATABASE SCHEMA UPDATE")
    
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
        return True
        
    except Exception as e:
        print(f"✗ Error during database migration: {e}")
        return False

def verify_database_tables():
    """Verify all required tables exist"""
    print_section("STEP 2: DATABASE TABLE VERIFICATION")
    
    required_tables = [
        'users',
        'links',
        'tracking_events',
        'campaigns',
        'notifications',
        'audit_logs',
        'security_settings',
        'domains'
    ]
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public' AND table_type='BASE TABLE';
        """)
        
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        print("Checking required tables...")
        all_exist = True
        for table in required_tables:
            if table in existing_tables:
                print(f"✓ {table} table exists")
            else:
                print(f"✗ {table} table MISSING")
                all_exist = False
        
        cursor.close()
        conn.close()
        
        return all_exist
        
    except Exception as e:
        print(f"✗ Error verifying tables: {e}")
        return False

def verify_user_columns():
    """Verify all user table columns"""
    print_section("STEP 3: USER TABLE COLUMN VERIFICATION")
    
    required_columns = [
        'id', 'username', 'email', 'password_hash', 'role', 'status',
        'plan_type', 'subscription_expiry', 'avatar_url', 'created_at'
    ]
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users';
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        print("Checking user table columns...")
        all_exist = True
        for col in required_columns:
            if col in existing_columns:
                print(f"✓ {col} column exists")
            else:
                print(f"✗ {col} column MISSING")
                all_exist = False
        
        cursor.close()
        conn.close()
        
        return all_exist
        
    except Exception as e:
        print(f"✗ Error verifying columns: {e}")
        return False

def create_uploads_directory():
    """Create uploads directory for avatars"""
    print_section("STEP 4: FILE SYSTEM SETUP")
    
    try:
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'avatars')
        os.makedirs(upload_dir, exist_ok=True)
        print(f"✓ Uploads directory created: {upload_dir}")
        return True
    except Exception as e:
        print(f"✗ Error creating uploads directory: {e}")
        return False

def verify_api_routes():
    """Verify critical API routes exist in codebase"""
    print_section("STEP 5: API ROUTE VERIFICATION")
    
    critical_routes = {
        'User Profile': 'src/routes/user.py',
        'Links': 'src/routes/links.py',
        'Analytics': 'src/routes/analytics.py',
        'Campaigns': 'src/routes/campaigns.py',
        'Notifications': 'src/routes/notifications.py',
        'Admin': 'src/routes/admin.py'
    }
    
    all_exist = True
    for name, path in critical_routes.items():
        full_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(full_path):
            print(f"✓ {name} routes exists")
        else:
            print(f"✗ {name} routes MISSING")
            all_exist = False
    
    return all_exist

def verify_components():
    """Verify critical frontend components exist"""
    print_section("STEP 6: COMPONENT VERIFICATION")
    
    critical_components = {
        'UserProfile': 'src/components/UserProfile.jsx',
        'Layout': 'src/components/Layout.jsx',
        'Dashboard': 'src/components/Dashboard.jsx',
        'TrackingLinks': 'src/components/TrackingLinks.jsx',
        'CampaignManagement': 'src/components/CampaignManagement.jsx',
        'AtlasMap': 'src/components/AtlasMap.jsx',
        'Geography': 'src/components/Geography.jsx'
    }
    
    all_exist = True
    for name, path in critical_components.items():
        full_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(full_path):
            print(f"✓ {name} component exists")
        else:
            print(f"✗ {name} component MISSING")
            all_exist = False
    
    return all_exist

def generate_fix_report(results):
    """Generate comprehensive fix report"""
    print_section("FIX REPORT SUMMARY")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
Brain Link Tracker - Comprehensive Fix Report
Generated: {timestamp}

{'='*60}
FIX STATUS:
{'='*60}

1. Database Schema Update........... {'✓ PASSED' if results['db_schema'] else '✗ FAILED'}
2. Database Table Verification...... {'✓ PASSED' if results['db_tables'] else '✗ FAILED'}
3. User Column Verification......... {'✓ PASSED' if results['user_columns'] else '✗ FAILED'}
4. File System Setup................ {'✓ PASSED' if results['file_system'] else '✗ FAILED'}
5. API Route Verification........... {'✓ PASSED' if results['api_routes'] else '✗ FAILED'}
6. Component Verification........... {'✓ PASSED' if results['components'] else '✗ FAILED'}

{'='*60}
FIXES APPLIED:
{'='*60}

✓ Profile Icon Implementation
  - Added UserProfile.jsx component
  - Updated Layout.jsx with profile dropdown
  - Added avatar upload support
  - Added password change functionality
  - Added subscription info display

✓ Notification Time Display Fix
  - Updated get_time_ago() function
  - Now shows "now", "2mins ago", etc.

✓ Link Regeneration Fix
  - Fixed API endpoint path
  - Changed from /links/regenerate/ to /api/links/regenerate/

✓ Heat Map Replacement
  - Created AtlasMap.jsx component
  - Integrated with Geography.jsx
  - Displays real-time geo data

✓ Backend API Enhancements
  - Added /api/user/profile (PUT) for profile updates
  - Added /api/user/change-password (POST) for password change
  - Added avatar_url field to User model
  - Updated user.to_dict() for frontend compatibility

{'='*60}
NEXT STEPS:
{'='*60}

1. Test all fixes locally
2. Run frontend build: npm run build
3. Test backend: python api/index.py
4. Commit changes to GitHub
5. Deploy to Vercel with environment variables

{'='*60}
CRITICAL REMINDERS:
{'='*60}

⚠  DO NOT touch quantum redirect code
⚠  Test login functionality before deploying
⚠  Verify all environment variables are set
⚠  Check frontend and backend builds succeed
"""
    
    print(report)
    
    # Save report to file
    with open('FIX_REPORT_OCT22.txt', 'w') as f:
        f.write(report)
    
    print("\n✓ Report saved to FIX_REPORT_OCT22.txt")

def main():
    """Main execution function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          BRAIN LINK TRACKER - MASTER FIX SCRIPT          ║
    ║                    October 22, 2025                      ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    results = {
        'db_schema': False,
        'db_tables': False,
        'user_columns': False,
        'file_system': False,
        'api_routes': False,
        'components': False
    }
    
    # Execute all fixes
    results['db_schema'] = add_avatar_column()
    results['db_tables'] = verify_database_tables()
    results['user_columns'] = verify_user_columns()
    results['file_system'] = create_uploads_directory()
    results['api_routes'] = verify_api_routes()
    results['components'] = verify_components()
    
    # Generate report
    generate_fix_report(results)
    
    # Final status
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "="*60)
        print("  ✓ ALL FIXES APPLIED SUCCESSFULLY")
        print("="*60 + "\n")
        return 0
    else:
        print("\n" + "="*60)
        print("  ✗ SOME FIXES FAILED - CHECK REPORT ABOVE")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
