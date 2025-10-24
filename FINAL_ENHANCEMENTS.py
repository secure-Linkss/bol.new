#!/usr/bin/env python3
"""
FINAL ENHANCEMENTS & POLISH
============================
Final touches to ensure everything works perfectly
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

print("=" * 80)
print("APPLYING FINAL ENHANCEMENTS")
print("=" * 80)

# =================================================================
# 1. Add Stripe.js to index.html
# =================================================================

print("\n[1/6] Adding Stripe.js to index.html...")

index_html_path = PROJECT_ROOT / 'index.html'
with open(index_html_path, 'r') as f:
    html_content = f.read()

if 'stripe.com/v3' not in html_content:
    # Add Stripe.js before closing </head>
    html_content = html_content.replace(
        '</head>',
        '  <script src="https://js.stripe.com/v3/"></script>\n  </head>'
    )
    
    with open(index_html_path, 'w') as f:
        f.write(html_content)
    
    print("  ✓ Added Stripe.js script to index.html")
else:
    print("  ✓ Stripe.js already in index.html")

# =================================================================
# 2. Add catch-all route to App.jsx
# =================================================================

print("\n[2/6] Adding catch-all route to App.jsx...")

app_jsx_path = PROJECT_ROOT / 'src' / 'App.jsx'
with open(app_jsx_path, 'r') as f:
    app_content = f.read()

# Check if catch-all exists
if 'path="*"' not in app_content and 'path={"*"}' not in app_content:
    # Add catch-all route before </Routes>
    catch_all_route = '''                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
'''
    
    app_content = app_content.replace(
        '                </Routes>',
        catch_all_route + '                </Routes>'
    )
    
    with open(app_jsx_path, 'w') as f:
        f.write(app_content)
    
    print("  ✓ Added catch-all route to App.jsx")
else:
    print("  ✓ Catch-all route already exists")

# =================================================================
# 3. Create comprehensive database initialization script
# =================================================================

print("\n[3/6] Creating comprehensive database initialization...")

db_init_content = '''#!/usr/bin/env python3
"""
Comprehensive Database Initialization
Ensures all tables and relationships exist in production
"""

import os
import sys
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.link import Link
from src.models.campaign import Campaign
from src.models.tracking_event import TrackingEvent
from src.models.audit_log import AuditLog
from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
from src.models.support_ticket import SupportTicket
from src.models.subscription_verification import SubscriptionVerification
from src.models.notification import Notification
from src.models.domain import Domain
from src.models.security_threat import SecurityThreat

def init_database():
    """Initialize all database tables"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL not set in environment")
        sys.exit(1)
    
    print(f"Connecting to database...")
    engine = create_engine(database_url)
    
    # Create all tables
    print("Creating all tables...")
    from api.index import app
    with app.app_context():
        db.create_all()
    
    print("✓ Database initialization complete")
    
    # Verify tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\nTables created: {len(tables)}")
    for table in sorted(tables):
        print(f"  - {table}")
    
    # Create default admin if not exists
    print("\nChecking default admin...")
    with app.app_context():
        if not User.query.filter_by(username="Brain").first():
            admin = User(
                username="Brain",
                email="admin@brainlinktracker.com",
                role="main_admin",
                status="active",
                is_active=True,
                is_verified=True
            )
            admin.set_password("Mayflower1!!")
            db.session.add(admin)
            db.session.commit()
            print("✓ Created default admin: Brain")
        else:
            print("✓ Default admin already exists")

if __name__ == '__main__':
    init_database()
'''

db_init_path = PROJECT_ROOT / 'initialize_production_db.py'
with open(db_init_path, 'w') as f:
    f.write(db_init_content)

os.chmod(db_init_path, 0o755)
print(f"  ✓ Created {db_init_path}")

# =================================================================
# 4. Create GitHub deployment script
# =================================================================

print("\n[4/6] Creating GitHub deployment script...")

deploy_script_content = '''#!/bin/bash

echo "===================================="
echo "BRAIN LINK TRACKER - DEPLOYMENT"
echo "===================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "ERROR: Not a git repository"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Detected changes, committing..."
    
    git add .
    
    echo "Enter commit message (or press Enter for default):"
    read commit_msg
    
    if [ -z "$commit_msg" ]; then
        commit_msg="Production deployment: Critical fixes and enhancements"
    fi
    
    git commit -m "$commit_msg"
    echo "✓ Changes committed"
else
    echo "✓ No uncommitted changes"
fi

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git push origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Next steps:"
    echo "1. Vercel will automatically deploy from GitHub"
    echo "2. Monitor deployment at: https://vercel.com/dashboard"
    echo "3. Check logs for any errors"
    echo "4. Test the deployment at: https://bolnew-sigma.vercel.app"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "1. Git credentials are correct"
    echo "2. Remote repository is accessible"
    echo "3. You have push permissions"
    echo ""
    exit 1
fi
'''

deploy_script_path = PROJECT_ROOT / 'deploy_to_github.sh'
with open(deploy_script_path, 'w') as f:
    f.write(deploy_script_content)

os.chmod(deploy_script_path, 0o755)
print(f"  ✓ Created {deploy_script_path}")

# =================================================================
# 5. Create comprehensive test script
# =================================================================

print("\n[5/6] Creating comprehensive test script...")

test_script_content = '''#!/usr/bin/env python3
"""
Comprehensive System Test
Tests all critical endpoints and functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://bolnew-sigma.vercel.app"  # Update if different
# For local testing, use: BASE_URL = "http://localhost:5173"

def test_login():
    """Test admin login"""
    print("\n[TEST] Admin Login...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "Brain",
        "password": "Mayflower1!!"
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✓ Login successful")
            return data.get('token')
        else:
            print(f"✗ Login failed: {data.get('error')}")
            return None
    else:
        print(f"✗ Login request failed: {response.status_code}")
        return None

def test_dashboard(token):
    """Test dashboard endpoint"""
    print("\n[TEST] Dashboard Stats...")
    response = requests.get(
        f"{BASE_URL}/api/admin/dashboard/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Dashboard stats retrieved")
        print(f"  Total Users: {data.get('total_users', 0)}")
        print(f"  Total Links: {data.get('total_links', 0)}")
        print(f"  Total Clicks: {data.get('total_clicks', 0)}")
        return True
    else:
        print(f"✗ Dashboard request failed: {response.status_code}")
        return False

def test_geographic_data(token):
    """Test geographic distribution"""
    print("\n[TEST] Geographic Distribution...")
    response = requests.get(
        f"{BASE_URL}/api/analytics/geographic-distribution",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            countries = data.get('countries', [])
            print(f"✓ Geographic data retrieved: {len(countries)} countries")
            return True
        else:
            print(f"✗ Geographic data failed: {data.get('error')}")
            return False
    else:
        print(f"✗ Geographic request failed: {response.status_code}")
        return False

def test_campaigns(token):
    """Test campaigns endpoint"""
    print("\n[TEST] Campaigns...")
    response = requests.get(
        f"{BASE_URL}/api/admin/campaigns",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        campaigns = data.get('campaigns', [])
        print(f"✓ Campaigns retrieved: {len(campaigns)} campaigns")
        return True
    else:
        print(f"✗ Campaigns request failed: {response.status_code}")
        return False

def main():
    print("=" * 60)
    print("BRAIN LINK TRACKER - SYSTEM TEST")
    print("=" * 60)
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    token = test_login()
    
    if token:
        test_dashboard(token)
        test_geographic_data(token)
        test_campaigns(token)
        
        print("\n" + "=" * 60)
        print("TEST SUITE COMPLETED")
        print("=" * 60)
    else:
        print("\n✗ Tests aborted - login failed")

if __name__ == '__main__':
    main()
'''

test_script_path = PROJECT_ROOT / 'test_production.py'
with open(test_script_path, 'w') as f:
    f.write(test_script_content)

os.chmod(test_script_path, 0o755)
print(f"  ✓ Created {test_script_path}")

# =================================================================
# 6. Create final deployment instructions
# =================================================================

print("\n[6/6] Creating final deployment instructions...")

final_instructions = '''
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BRAIN LINK TRACKER - DEPLOYMENT READY                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

✅ ALL CRITICAL FIXES APPLIED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ✓ Stripe payment integration (backend + frontend)
2. ✓ Geography map component fixed
3. ✓ Campaign auto-creation logic implemented
4. ✓ Geographic distribution API endpoint added
5. ✓ Stripe.js added to index.html
6. ✓ Catch-all route added to App.jsx
7. ✓ Profile dropdown already functional in Layout.jsx
8. ✓ Stripe blueprint registered in api/index.py
9. ✓ All dependencies updated in requirements.txt
10. ✓ Production .env file created

📋 DEPLOYMENT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Initialize Production Database
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run this to ensure all tables exist:

    python3 initialize_production_db.py

STEP 2: Test Locally (Optional but Recommended)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before deploying, test everything works:

    # Install dependencies
    npm install --legacy-peer-deps

    # Run development server
    npm run dev

    # Test in browser at http://localhost:5173
    # Login as: Brain / Mayflower1!!

STEP 3: Deploy to GitHub
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Use the deployment script:

    ./deploy_to_github.sh

Or manually:

    git add .
    git commit -m "Production deployment: All critical fixes applied"
    git push origin master

STEP 4: Configure Vercel Environment Variables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Go to: https://vercel.com/dashboard → Your Project → Settings → Environment Variables

Add these variables (from .env file):

    DATABASE_URL=postgresql://neondb_owner:npg_7CcKbPRm2GDw@...
    SECRET_KEY=ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE
    SHORTIO_API_KEY=sk_DbGGlUHPN7Z9VotL
    SHORTIO_DOMAIN=Secure-links.short.gy
    STRIPE_SECRET_KEY=sk_test_your_test_key_here
    STRIPE_PUBLISHABLE_KEY=pk_test_your_test_key_here
    APP_URL=https://bolnew-sigma.vercel.app

Make sure to set them for "Production" environment!

STEP 5: Trigger Vercel Deployment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vercel should auto-deploy when you push to GitHub.

Or manually trigger:
    
    vercel --prod

STEP 6: Post-Deployment Testing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run the comprehensive test script:

    python3 test_production.py

Or test manually:
    1. Visit: https://bolnew-sigma.vercel.app
    2. Login as: Brain / Mayflower1!!
    3. Test each tab:
       - Dashboard (check metrics)
       - Tracking Links (create a link)
       - Campaign (verify auto-creation)
       - Geography (check map displays)
       - Admin Panel (check all tabs load)
    4. Test profile dropdown (click avatar in header)
    5. Refresh page (should not white screen)

🔍 WHAT WAS FIXED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FRONTEND:
- Geography.jsx: Complete rewrite with proper map rendering
- StripePaymentForm.jsx: New component for Stripe checkout
- App.jsx: Added catch-all route to prevent 404 on refresh
- index.html: Added Stripe.js script tag
- Layout.jsx: Already had working profile dropdown (no changes needed)

BACKEND:
- stripe_payments.py: NEW - Full Stripe integration
- campaigns.py: Added auto_create_campaign helper function
- links.py: Updated to use campaign auto-creation
- analytics.py: Added geographic-distribution endpoint
- api/index.py: Registered Stripe blueprint

CONFIGURATION:
- .env: Production credentials configured
- vercel.json: Already correctly configured for SPA routing
- requirements.txt: Stripe dependency added

⚠️ REMAINING MANUAL TASKS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

These are enhancements that require careful manual implementation:

1. AdminPanelComplete.jsx (2846 lines):
   - Add Stripe payment tab alongside crypto
   - Expand User Management tab with requested columns
   - Add Pending Users table
   - Add Suspended Accounts section
   - Expand Security tab with more columns
   - Add Bot Activity Logs
   - Merge payment configuration into Settings tab

2. Stripe Configuration:
   - Create Stripe account and products
   - Get real API keys (currently using test keys)
   - Configure webhook endpoint

3. Campaign Auto-Creation Testing:
   - Verify the logic works correctly
   - Test with various scenarios

4. Metrics Consistency:
   - Verify dashboard and links show same data
   - Check TrackingEvent.is_bot filtering

🎯 EXPECTED RESULTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After deployment:
✓ Login works correctly
✓ All tabs load without errors
✓ Geography map displays with data
✓ Dashboard shows real metrics
✓ Links can be created
✓ Campaigns auto-create
✓ Profile dropdown works (click avatar)
✓ Page refresh maintains current route (no white screen)
✓ Stripe payment flow initiates (test mode)

🆘 TROUBLESHOOTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If geography map is blank:
- Check browser console for errors
- Verify TrackingEvent table has country data
- Check /api/analytics/geographic-distribution endpoint

If white screen on refresh:
- Check Vercel build logs
- Verify vercel.json routes are correct
- Check browser console for errors

If metrics don't match:
- Check is_bot filtering in queries
- Verify same time range is used
- Check TrackingEvent data consistency

If Stripe doesn't work:
- Verify STRIPE_SECRET_KEY is set in Vercel
- Check browser console for Stripe.js load errors
- Verify Stripe.js script is in index.html

📞 SUPPORT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you encounter issues:
1. Check Vercel deployment logs
2. Check browser console errors
3. Check Network tab in browser DevTools
4. Review database logs
5. Test API endpoints directly

════════════════════════════════════════════════════════════════════════════════
                              🚀 READY TO DEPLOY! 🚀
════════════════════════════════════════════════════════════════════════════════

Run: ./deploy_to_github.sh

════════════════════════════════════════════════════════════════════════════════
'''

instructions_path = PROJECT_ROOT / 'DEPLOYMENT_INSTRUCTIONS_FINAL.txt'
with open(instructions_path, 'w') as f:
    f.write(final_instructions)

print(f"  ✓ Created {instructions_path}")

print("\n" + "=" * 80)
print("FINAL ENHANCEMENTS COMPLETED!")
print("=" * 80)
print(f"\n📖 Read deployment instructions:")
print(f"   {instructions_path}")
print("\n🚀 Ready to deploy! Run: ./deploy_to_github.sh")
print("=" * 80)
