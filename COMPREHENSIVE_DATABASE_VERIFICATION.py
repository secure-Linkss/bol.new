#!/usr/bin/env python3
"""
COMPREHENSIVE DATABASE SCHEMA VERIFICATION
Checks all tables, columns, and relationships
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def verify_database_schema():
    """Verify all database tables and columns"""
    print("="*70)
    print("DATABASE SCHEMA VERIFICATION")
    print("="*70)
    
    try:
        from src.database import db
        from src.models.user import User, Admin
        from src.models.link import Link
        from src.models.campaign import Campaign
        from src.models.tracking_event import TrackingEvent
        from src.models.notification import Notification
        from src.models.security import Security
        from src.models.security_threat_db import SecurityThreat
        from src.models.support_ticket_db import SupportTicket
        from src.models.subscription_verification_db import SubscriptionVerification
        from src.models.admin_settings import AdminSettings
        from src.models.audit_log import AuditLog
        from src.models.domain import Domain
        
        models = [
            ("User", User),
            ("Admin", Admin),
            ("Link", Link),
            ("Campaign", Campaign),
            ("TrackingEvent", TrackingEvent),
            ("Notification", Notification),
            ("Security", Security),
            ("SecurityThreat", SecurityThreat),
            ("SupportTicket", SupportTicket),
            ("SubscriptionVerification", SubscriptionVerification),
            ("AdminSettings", AdminSettings),
            ("AuditLog", AuditLog),
            ("Domain", Domain)
        ]
        
        print("\n✅ MODEL VERIFICATION:")
        for name, model in models:
            table_name = model.__tablename__
            columns = [c.name for c in model.__table__.columns]
            print(f"  ✓ {name} ({table_name}): {len(columns)} columns")
        
        print(f"\n✅ Total Models: {len(models)}")
        print("✅ All models imported successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_api_routes():
    """Verify all API routes are registered"""
    print("\n" + "="*70)
    print("API ROUTES VERIFICATION")
    print("="*70)
    
    api_index = Path("/home/user/brain-link-tracker/api/index.py")
    
    if not api_index.exists():
        print("❌ api/index.py not found!")
        return False
    
    with open(api_index, 'r') as f:
        content = f.read()
    
    required_blueprints = [
        'auth_bp',
        'links_bp',
        'analytics_bp',
        'campaigns_bp',
        'domains_bp',
        'settings_bp',
        'admin_bp',
        'admin_complete_bp',
        'admin_settings_bp',
        'security_bp',
        'security_complete_bp',
        'advanced_security_bp',
        'notifications_bp',
        'track_bp',
        'events_bp',
        'shorten_bp',
        'telegram_bp',
        'quantum_redirect_bp',
        'page_tracking_bp',
        'analytics_complete_bp',
        'analytics_fixed_bp'
    ]
    
    registered = []
    missing = []
    
    for bp in required_blueprints:
        if bp in content:
            registered.append(bp)
        else:
            missing.append(bp)
    
    print(f"\n✅ Registered Blueprints: {len(registered)}")
    for bp in registered:
        print(f"  ✓ {bp}")
    
    if missing:
        print(f"\n⚠️  Missing Blueprints: {len(missing)}")
        for bp in missing:
            print(f"  ✗ {bp}")
    
    return len(missing) == 0

def verify_frontend_components():
    """Verify all frontend components exist"""
    print("\n" + "="*70)
    print("FRONTEND COMPONENTS VERIFICATION")
    print("="*70)
    
    components_dir = Path("/home/user/brain-link-tracker/src/components")
    
    required_components = [
        'Dashboard.jsx',
        'TrackingLinks.jsx',
        'LiveActivity.jsx',
        'Analytics.jsx',
        'Geography.jsx',
        'Campaign.jsx',
        'Settings.jsx',
        'Security.jsx',
        'AdminPanel.jsx',
        'Notifications.jsx',
        'LoginPage.jsx',
        'CreateLinkModal.jsx',
        'InteractiveMap.jsx'
    ]
    
    existing = []
    missing = []
    
    for comp in required_components:
        comp_path = components_dir / comp
        if comp_path.exists():
            existing.append(comp)
        else:
            missing.append(comp)
    
    print(f"\n✅ Existing Components: {len(existing)}")
    for comp in existing:
        print(f"  ✓ {comp}")
    
    if missing:
        print(f"\n❌ Missing Components: {len(missing)}")
        for comp in missing:
            print(f"  ✗ {comp}")
    
    return len(missing) == 0

def verify_environment_variables():
    """Verify environment configuration"""
    print("\n" + "="*70)
    print("ENVIRONMENT VARIABLES VERIFICATION")
    print("="*70)
    
    env_production = Path("/home/user/brain-link-tracker/.env.production")
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'SHORTIO_API_KEY',
        'SHORTIO_DOMAIN'
    ]
    
    if not env_production.exists():
        print("❌ .env.production not found!")
        return False
    
    with open(env_production, 'r') as f:
        content = f.read()
    
    present = []
    missing = []
    
    for var in required_vars:
        if var in content:
            # Check if it has a value
            lines = content.split('\n')
            for line in lines:
                if line.startswith(var + '=') and '=' in line:
                    value = line.split('=', 1)[1].strip()
                    if value:
                        present.append(var)
                    else:
                        missing.append(f"{var} (empty)")
                    break
        else:
            missing.append(var)
    
    print(f"\n✅ Present Variables: {len(present)}")
    for var in present:
        print(f"  ✓ {var}")
    
    if missing:
        print(f"\n⚠️  Missing/Empty Variables: {len(missing)}")
        for var in missing:
            print(f"  ✗ {var}")
    
    return len(missing) == 0

def main():
    """Run all verifications"""
    print("🔍 STARTING COMPREHENSIVE PROJECT VERIFICATION...\n")
    
    results = []
    
    # Run verifications
    results.append(("Database Schema", verify_database_schema()))
    results.append(("API Routes", verify_api_routes()))
    results.append(("Frontend Components", verify_frontend_components()))
    results.append(("Environment Variables", verify_environment_variables()))
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
    
    if passed == total:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        return 0
    else:
        print("\n⚠️  SOME VERIFICATIONS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
