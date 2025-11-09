#!/usr/bin/env python3
"""
FULL PRODUCTION AUDIT SCRIPT
This script performs a comprehensive audit of the entire project
"""

import os
import sys
import json
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

def audit_frontend():
    """Audit frontend components and structure"""
    print("\n" + "="*80)
    print("FRONTEND AUDIT")
    print("="*80)
    
    components_dir = Path("src/components")
    if not components_dir.exists():
        print("❌ Components directory not found")
        return False
    
    # Check critical components
    critical_components = [
        "Layout.jsx",
        "Dashboard.jsx",
        "TrackingLinks.jsx",
        "AdminPanelComplete.jsx",
        "Settings.jsx",
        "Profile.jsx",
        "LoginPage.jsx"
    ]
    
    missing = []
    for comp in critical_components:
        comp_path = components_dir / comp
        if not comp_path.exists():
            missing.append(comp)
            print(f"❌ Missing: {comp}")
        else:
            print(f"✅ Found: {comp}")
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} critical components")
        return False
    
    print("\n✅ All critical frontend components exist")
    return True

def audit_backend():
    """Audit backend API routes and models"""
    print("\n" + "="*80)
    print("BACKEND AUDIT")
    print("="*80)
    
    # Check API routes
    routes_dir = Path("src/routes")
    if not routes_dir.exists():
        print("❌ Routes directory not found")
        return False
    
    critical_routes = [
        "auth.py",
        "user.py",
        "links.py",
        "analytics.py",
        "campaigns.py",
        "admin.py",
        "admin_complete.py",
        "settings.py",
        "profile.py"
    ]
    
    missing_routes = []
    for route in critical_routes:
        route_path = routes_dir / route
        if not route_path.exists():
            missing_routes.append(route)
            print(f"❌ Missing route: {route}")
        else:
            print(f"✅ Found route: {route}")
    
    # Check models
    models_dir = Path("src/models")
    if not models_dir.exists():
        print("❌ Models directory not found")
        return False
    
    critical_models = [
        "user.py",
        "link.py",
        "tracking_event.py",
        "campaign.py",
        "audit_log.py",
        "notification.py"
    ]
    
    missing_models = []
    for model in critical_models:
        model_path = models_dir / model
        if not model_path.exists():
            missing_models.append(model)
            print(f"❌ Missing model: {model}")
        else:
            print(f"✅ Found model: {model}")
    
    if missing_routes or missing_models:
        print(f"\n⚠️  Missing {len(missing_routes)} routes and {len(missing_models)} models")
        return False
    
    print("\n✅ All critical backend components exist")
    return True

def check_profile_avatar():
    """Check if profile avatar dropdown is properly implemented"""
    print("\n" + "="*80)
    print("PROFILE AVATAR DROPDOWN CHECK")
    print("="*80)
    
    layout_file = Path("src/components/Layout.jsx")
    if not layout_file.exists():
        print("❌ Layout.jsx not found")
        return False
    
    content = layout_file.read_text()
    
    checks = {
        "Avatar import": "@/components/ui/avatar" in content,
        "DropdownMenu import": "DropdownMenu" in content,
        "Avatar component used": "<Avatar" in content,
        "AvatarFallback": "AvatarFallback" in content,
        "Profile menu item": "Profile" in content or "profile" in content,
        "Logout menu item": "Logout" in content or "onLogout" in content,
        "User role display": "role" in content and "user.role" in content
    }
    
    all_passed = True
    for check, passed in checks.items():
        if passed:
            print(f"✅ {check}")
        else:
            print(f"❌ {check}")
            all_passed = False
    
    if all_passed:
        print("\n✅ Profile avatar dropdown is properly implemented")
    else:
        print("\n⚠️  Profile avatar dropdown has missing elements")
    
    return all_passed

def check_environment_setup():
    """Check if environment variables are properly configured"""
    print("\n" + "="*80)
    print("ENVIRONMENT CONFIGURATION CHECK")
    print("="*80)
    
    env_example = Path(".env.example")
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    content = env_example.read_text()
    
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "SHORTIO_API_KEY",
        "SHORTIO_DOMAIN",
        "STRIPE_SECRET_KEY",
        "STRIPE_PUBLISHABLE_KEY"
    ]
    
    all_present = True
    for var in required_vars:
        if var in content:
            print(f"✅ {var} configured")
        else:
            print(f"❌ {var} missing")
            all_present = False
    
    if all_present:
        print("\n✅ All required environment variables are documented")
    else:
        print("\n⚠️  Some environment variables are missing")
    
    return all_present

def check_build_config():
    """Check if build configuration is correct"""
    print("\n" + "="*80)
    print("BUILD CONFIGURATION CHECK")
    print("="*80)
    
    # Check package.json
    package_json = Path("package.json")
    if not package_json.exists():
        print("❌ package.json not found")
        return False
    
    try:
        with open(package_json) as f:
            data = json.load(f)
        
        if "scripts" in data and "build" in data["scripts"]:
            print(f"✅ Build script found: {data['scripts']['build']}")
        else:
            print("❌ Build script missing in package.json")
            return False
    except Exception as e:
        print(f"❌ Error reading package.json: {e}")
        return False
    
    # Check vercel.json
    vercel_json = Path("vercel.json")
    if not vercel_json.exists():
        print("❌ vercel.json not found")
        return False
    
    try:
        with open(vercel_json) as f:
            data = json.load(f)
        
        if "buildCommand" in data:
            print(f"✅ Vercel build command: {data['buildCommand']}")
        
        if "outputDirectory" in data:
            print(f"✅ Vercel output directory: {data['outputDirectory']}")
        else:
            print("❌ Output directory not configured in vercel.json")
            return False
    except Exception as e:
        print(f"❌ Error reading vercel.json: {e}")
        return False
    
    print("\n✅ Build configuration is correct")
    return True

def check_dist_folder():
    """Check if dist folder exists"""
    print("\n" + "="*80)
    print("DIST FOLDER CHECK")
    print("="*80)
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist folder does not exist - NEEDS TO BE BUILT")
        return False
    
    # Check for index.html
    index_html = dist_dir / "index.html"
    if not index_html.exists():
        print("❌ dist/index.html missing")
        return False
    
    print("✅ dist folder exists with index.html")
    
    # Check assets
    assets_dir = dist_dir / "assets"
    if assets_dir.exists():
        asset_files = list(assets_dir.glob("*"))
        print(f"✅ Found {len(asset_files)} asset files")
    else:
        print("⚠️  assets folder missing in dist")
    
    return True

def main():
    print("\n" + "="*80)
    print("BRAIN LINK TRACKER - FULL PRODUCTION AUDIT")
    print("="*80)
    
    results = {
        "Frontend Components": audit_frontend(),
        "Backend API & Models": audit_backend(),
        "Profile Avatar Dropdown": check_profile_avatar(),
        "Environment Configuration": check_environment_setup(),
        "Build Configuration": check_build_config(),
        "Dist Folder": check_dist_folder()
    }
    
    print("\n" + "="*80)
    print("AUDIT SUMMARY")
    print("="*80)
    
    all_passed = True
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL CHECKS PASSED - Ready for deployment")
    else:
        print("❌ SOME CHECKS FAILED - Fixes needed before deployment")
    print("="*80)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
