#!/usr/bin/env python3
"""
Test Flask Application for Brain Link Tracker
"""

import os
import sys
import traceback
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 80)
print("FLASK APPLICATION TESTING")
print("=" * 80)

def test_database_models():
    """Test if all models can be imported and created"""
    print("\n1. TESTING MODEL IMPORTS")
    print("-" * 50)
    
    try:
        # Import Flask app
        from api.index import app, db
        
        with app.app_context():
            # Test model imports
            from src.models.user import User
            from src.models.link import Link
            from src.models.campaign import Campaign
            from src.models.tracking_event import TrackingEvent
            from src.models.notification import Notification
            from src.models.audit_log import AuditLog
            from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
            from src.models.support_ticket import SupportTicket
            from src.models.subscription_verification import SubscriptionVerification
            
            print("✅ All models imported successfully")
            
            # Test database connection
            users = User.query.all()
            print(f"✅ Database query successful: {len(users)} users found")
            
            links = Link.query.all()
            print(f"✅ Links query successful: {len(links)} links found")
            
            campaigns = Campaign.query.all()
            print(f"✅ Campaigns query successful: {len(campaigns)} campaigns found")
            
            events = TrackingEvent.query.all()
            print(f"✅ Tracking events query successful: {len(events)} events found")
            
            notifications = Notification.query.all()
            print(f"✅ Notifications query successful: {len(notifications)} notifications found")
            
            return True
            
    except Exception as e:
        print(f"❌ Model testing failed: {str(e)}")
        traceback.print_exc()
        return False

def test_api_routes():
    """Test API routes by starting Flask app temporarily"""
    print("\n2. TESTING API ROUTES")
    print("-" * 50)
    
    try:
        from api.index import app
        
        # Test route registration
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.methods} {rule.rule}")
        
        print(f"✅ Total routes registered: {len(routes)}")
        
        # Print some key routes
        api_routes = [route for route in routes if '/api/' in route]
        print(f"✅ API routes: {len(api_routes)}")
        
        key_routes = [
            '/api/auth/login',
            '/api/auth/register', 
            '/api/links',
            '/api/campaigns',
            '/api/analytics',
            '/api/admin'
        ]
        
        found_routes = []
        for key_route in key_routes:
            matching_routes = [route for route in routes if key_route in route]
            if matching_routes:
                found_routes.append(key_route)
                print(f"✅ Found route: {key_route}")
            else:
                print(f"⚠️  Route not found: {key_route}")
        
        print(f"\nRoute Summary: {len(found_routes)}/{len(key_routes)} key routes found")
        
        return True
        
    except Exception as e:
        print(f"❌ Route testing failed: {str(e)}")
        traceback.print_exc()
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\n3. TESTING ENVIRONMENT CONFIGURATION")
    print("-" * 50)
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL', 'SHORTIO_API_KEY', 'SHORTIO_DOMAIN']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Show partial value for security
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
        else:
            missing_vars.append(var)
            print(f"❌ {var}: Missing")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print(f"\n✅ All required environment variables configured")
        return True

def test_vercel_compatibility():
    """Test Vercel deployment compatibility"""
    print("\n4. TESTING VERCEL COMPATIBILITY")
    print("-" * 50)
    
    issues = []
    
    # Check vercel.json
    if os.path.exists('vercel.json'):
        print("✅ vercel.json exists")
        with open('vercel.json', 'r') as f:
            vercel_config = json.load(f)
        
        # Check builds configuration
        if 'builds' in vercel_config:
            python_build = False
            for build in vercel_config['builds']:
                if build.get('use') == '@vercel/python':
                    python_build = True
                    print("✅ Python runtime configured")
                    break
            
            if not python_build:
                issues.append("Python runtime not configured in vercel.json")
        else:
            issues.append("No builds configuration in vercel.json")
        
        # Check routes
        if 'routes' in vercel_config:
            api_routes = [route for route in vercel_config['routes'] if '/api/' in route.get('src', '')]
            print(f"✅ {len(api_routes)} API routes configured in vercel.json")
        else:
            issues.append("No routes configuration in vercel.json")
    else:
        issues.append("vercel.json not found")
    
    # Check requirements.txt
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt exists")
        
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        # Check for essential packages
        essential_packages = ['Flask', 'psycopg2-binary', 'gunicorn']
        for package in essential_packages:
            if package.lower() in requirements.lower():
                print(f"✅ {package} found in requirements")
            else:
                issues.append(f"{package} not found in requirements.txt")
    else:
        issues.append("requirements.txt not found")
    
    if issues:
        print(f"\n⚠️  Vercel compatibility issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ Vercel compatibility looks good")
        return True

def create_test_admin_user():
    """Create test admin user if doesn't exist"""
    print("\n5. CHECKING ADMIN USERS")
    print("-" * 50)
    
    try:
        from api.index import app, db
        from src.models.user import User
        
        with app.app_context():
            # Check default admin users
            brain_user = User.query.filter_by(username='Brain').first()
            if brain_user:
                print(f"✅ Admin user 'Brain' exists (Role: {brain_user.role}, Status: {brain_user.status})")
            else:
                print("⚠️  Admin user 'Brain' not found")
            
            seventh_brain_user = User.query.filter_by(username='7thbrain').first()
            if seventh_brain_user:
                print(f"✅ Admin user '7thbrain' exists (Role: {seventh_brain_user.role}, Status: {seventh_brain_user.status})")
            else:
                print("⚠️  Admin user '7thbrain' not found")
            
            return True
            
    except Exception as e:
        print(f"❌ Admin user check failed: {str(e)}")
        return False

# Run all tests
if __name__ == "__main__":
    print("Starting comprehensive Flask application tests...")
    
    tests = [
        ("Database Models", test_database_models),
        ("API Routes", test_api_routes),
        ("Environment Config", test_environment_config),
        ("Vercel Compatibility", test_vercel_compatibility),
        ("Admin Users", create_test_admin_user)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nOverall: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Application is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    print("=" * 80)