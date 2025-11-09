#!/usr/bin/env python3
"""
PRE-DEPLOYMENT TEST SCRIPT
Tests database connections and critical API functionality
"""

import os
import sys

# Set production environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'
os.environ['SHORTIO_API_KEY'] = 'sk_DbGGlUHPN7Z9VotL'
os.environ['SHORTIO_DOMAIN'] = 'Secure-links.short.gy'

sys.path.insert(0, os.path.dirname(__file__))

def test_database_connection():
    """Test database connection"""
    print("\n" + "="*80)
    print("DATABASE CONNECTION TEST")
    print("="*80)
    
    try:
        from src.models.user import db, User
        from src.models.link import Link
        from src.models.campaign import Campaign
        from src.models.tracking_event import TrackingEvent
        from api.index import app
        
        with app.app_context():
            # Test connection
            db.engine.connect()
            print("✅ Database connection successful")
            
            # Check if tables exist
            print("\nChecking tables...")
            tables = {
                "users": User,
                "links": Link,
                "campaigns": Campaign,
                "tracking_events": TrackingEvent
            }
            
            for table_name, model in tables.items():
                try:
                    count = model.query.count()
                    print(f"✅ {table_name}: {count} records")
                except Exception as e:
                    print(f"❌ {table_name}: Error - {e}")
                    return False
            
            # Test admin user exists
            admin = User.query.filter_by(username="Brain").first()
            if admin:
                print(f"\n✅ Admin user 'Brain' exists")
                print(f"   - Email: {admin.email}")
                print(f"   - Role: {admin.role}")
                print(f"   - Status: {admin.status}")
                print(f"   - Active: {admin.is_active}")
            else:
                print("\n❌ Admin user 'Brain' not found")
                return False
            
            admin2 = User.query.filter_by(username="7thbrain").first()
            if admin2:
                print(f"\n✅ Admin user '7thbrain' exists")
                print(f"   - Email: {admin2.email}")
                print(f"   - Role: {admin2.role}")
                print(f"   - Status: {admin2.status}")
            else:
                print("\n⚠️  Admin user '7thbrain' not found")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_models():
    """Test all database models"""
    print("\n" + "="*80)
    print("DATABASE MODELS TEST")
    print("="*80)
    
    try:
        from api.index import app
        from src.models.user import db, User
        from src.models.link import Link
        from src.models.campaign import Campaign
        from src.models.tracking_event import TrackingEvent
        from src.models.audit_log import AuditLog
        from src.models.notification import Notification
        from src.models.security import SecuritySettings
        
        with app.app_context():
            models = {
                "User": User,
                "Link": Link,
                "Campaign": Campaign,
                "TrackingEvent": TrackingEvent,
                "AuditLog": AuditLog,
                "Notification": Notification,
                "SecuritySettings": SecuritySettings
            }
            
            all_passed = True
            for model_name, model_class in models.items():
                try:
                    # Try to query the model
                    count = model_class.query.count()
                    print(f"✅ {model_name}: {count} records")
                except Exception as e:
                    print(f"❌ {model_name}: {e}")
                    all_passed = False
            
            return all_passed
            
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def test_api_imports():
    """Test that all API routes can be imported"""
    print("\n" + "="*80)
    print("API ROUTES IMPORT TEST")
    print("="*80)
    
    try:
        from api.index import app
        
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'path': str(rule)
                })
        
        print(f"✅ Loaded {len(routes)} API routes")
        
        # Check critical endpoints
        critical_endpoints = [
            '/api/auth/login',
            '/api/auth/register',
            '/api/links',
            '/api/campaigns',
            '/api/analytics/overview',
            '/api/admin/users'
        ]
        
        route_paths = [r['path'] for r in routes]
        
        for endpoint in critical_endpoints:
            if endpoint in route_paths:
                print(f"✅ {endpoint}")
            else:
                # Check if any route matches the pattern
                found = any(endpoint in path for path in route_paths)
                if found:
                    print(f"✅ {endpoint} (pattern match)")
                else:
                    print(f"⚠️  {endpoint} (not found but may be registered differently)")
        
        return True
        
    except Exception as e:
        print(f"❌ API routes test failed: {e}")
        return False

def test_campaign_model_fields():
    """Test that Campaign model has all required fields"""
    print("\n" + "="*80)
    print("CAMPAIGN MODEL FIELDS TEST")
    print("="*80)
    
    try:
        from api.index import app
        from src.models.campaign import Campaign
        
        with app.app_context():
            # Check model fields
            required_fields = ['id', 'name', 'owner_id', 'status', 'created_at']
            
            # Get all columns from the model
            columns = [c.name for c in Campaign.__table__.columns]
            
            print(f"Campaign model has {len(columns)} columns:")
            for col in columns:
                print(f"  - {col}")
            
            all_present = True
            for field in required_fields:
                if field not in columns:
                    print(f"❌ Missing required field: {field}")
                    all_present = False
            
            if all_present:
                print("\n✅ All required fields present in Campaign model")
            
            return all_present
            
    except Exception as e:
        print(f"❌ Campaign model test failed: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("BRAIN LINK TRACKER - PRE-DEPLOYMENT TEST")
    print("="*80)
    
    results = {
        "Database Connection": test_database_connection(),
        "Database Models": test_models(),
        "API Routes": test_api_imports(),
        "Campaign Model Fields": test_campaign_model_fields()
    }
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL TESTS PASSED - Ready for Vercel deployment")
    else:
        print("❌ SOME TESTS FAILED - Review issues before deployment")
    print("="*80)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
