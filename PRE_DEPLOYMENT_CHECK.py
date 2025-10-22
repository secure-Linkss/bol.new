#!/usr/bin/env python3
"""
PRE-DEPLOYMENT CHECK SCRIPT
===========================
Comprehensive checks before deploying to production
"""

import os
import json
import sys

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_env_variables():
    """Check if all environment variables are set"""
    print_header("ENVIRONMENT VARIABLES CHECK")
    
    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'SHORTIO_API_KEY',
        'SHORTIO_DOMAIN'
    ]
    
    # Check .env file
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✓ .env file exists")
        with open(env_file, 'r') as f:
            content = f.read()
            all_present = all(var in content for var in required_vars)
            if all_present:
                print("✓ All required environment variables present")
                return True
            else:
                print("✗ Some environment variables missing")
                return False
    else:
        print(f"✗ .env file not found")
        return False

def check_critical_files():
    """Check if all critical files are present"""
    print_header("CRITICAL FILES CHECK")
    
    files = {
        'Backend': [
            'api/index.py',
            'src/routes/user.py',
            'src/routes/links.py',
            'src/routes/analytics.py',
            'src/routes/campaigns.py',
            'src/routes/notifications.py',
            'src/models/user.py',
            'src/models/link.py',
            'src/models/notification.py'
        ],
        'Frontend': [
            'src/components/UserProfile.jsx',
            'src/components/Layout.jsx',
            'src/components/TrackingLinks.jsx',
            'src/components/CampaignManagement.jsx',
            'src/components/AtlasMap.jsx',
            'src/components/Geography.jsx',
            'src/components/Dashboard.jsx'
        ],
        'Configuration': [
            'package.json',
            'requirements.txt',
            'vercel.json',
            '.gitignore'
        ]
    }
    
    all_present = True
    for category, file_list in files.items():
        print(f"\n{category}:")
        for file in file_list:
            if not check_file_exists(file, os.path.basename(file)):
                all_present = False
    
    return all_present

def check_code_quality():
    """Check for common code issues"""
    print_header("CODE QUALITY CHECK")
    
    issues = []
    
    # Check TrackingLinks.jsx for correct endpoint
    tracking_links_file = 'src/components/TrackingLinks.jsx'
    if os.path.exists(tracking_links_file):
        with open(tracking_links_file, 'r') as f:
            content = f.read()
            if '/api/links/regenerate/' in content:
                print("✓ TrackingLinks.jsx: Correct regenerate endpoint")
            else:
                print("✗ TrackingLinks.jsx: Incorrect regenerate endpoint")
                issues.append("TrackingLinks regenerate endpoint")
    
    # Check notifications.py for updated time function
    notifications_file = 'src/routes/notifications.py'
    if os.path.exists(notifications_file):
        with open(notifications_file, 'r') as f:
            content = f.read()
            if 'total_seconds' in content:
                print("✓ notifications.py: Updated get_time_ago function")
            else:
                print("✗ notifications.py: Old get_time_ago function")
                issues.append("Notifications time function")
    
    # Check User model for avatar_url
    user_model_file = 'src/models/user.py'
    if os.path.exists(user_model_file):
        with open(user_model_file, 'r') as f:
            content = f.read()
            if 'avatar_url' in content:
                print("✓ user.py: avatar_url field present")
            else:
                print("✗ user.py: avatar_url field missing")
                issues.append("User model avatar_url")
    
    # Check Layout for UserProfile import
    layout_file = 'src/components/Layout.jsx'
    if os.path.exists(layout_file):
        with open(layout_file, 'r') as f:
            content = f.read()
            if 'UserProfile' in content:
                print("✓ Layout.jsx: UserProfile integrated")
            else:
                print("✗ Layout.jsx: UserProfile not integrated")
                issues.append("Layout UserProfile integration")
    
    return len(issues) == 0

def check_build_files():
    """Check if build output exists"""
    print_header("BUILD FILES CHECK")
    
    build_dir = 'dist'
    if os.path.exists(build_dir):
        files = os.listdir(build_dir)
        if 'index.html' in files:
            print(f"✓ Build directory exists with {len(files)} files")
            return True
        else:
            print("✗ Build directory incomplete")
            return False
    else:
        print("✗ Build directory not found")
        return False

def check_package_json():
    """Verify package.json structure"""
    print_header("PACKAGE.JSON CHECK")
    
    if os.path.exists('package.json'):
        with open('package.json', 'r') as f:
            data = json.load(f)
            
            # Check scripts
            if 'build' in data.get('scripts', {}):
                print("✓ Build script present")
            else:
                print("✗ Build script missing")
                return False
            
            # Check key dependencies
            required_deps = ['react', 'react-dom', 'react-router-dom', 'lucide-react']
            missing = []
            for dep in required_deps:
                if dep in data.get('dependencies', {}):
                    print(f"✓ {dep} dependency present")
                else:
                    print(f"✗ {dep} dependency missing")
                    missing.append(dep)
            
            return len(missing) == 0
    else:
        print("✗ package.json not found")
        return False

def check_quantum_redirect():
    """Verify quantum redirect code is untouched"""
    print_header("QUANTUM REDIRECT VERIFICATION")
    
    quantum_file = 'src/routes/quantum_redirect.py'
    if os.path.exists(quantum_file):
        print(f"✓ quantum_redirect.py exists and untouched")
        return True
    else:
        print(f"✗ quantum_redirect.py not found")
        return False

def generate_checklist():
    """Generate deployment checklist"""
    print_header("DEPLOYMENT CHECKLIST")
    
    checklist = """
    BEFORE DEPLOYING:
    □ All environment variables configured
    □ Frontend build successful (npm run build)
    □ Backend tests passed
    □ All API endpoints verified
    □ Database migrations completed
    □ Git changes committed
    
    AFTER DEPLOYING:
    □ Test login with all accounts
    □ Verify profile icon functionality
    □ Test link regeneration
    □ Check notification time display
    □ Verify atlas map rendering
    □ Test all 9 user tabs
    □ Test all admin sub-tabs
    □ Verify campaign auto-creation
    □ Check page reload behavior
    □ Monitor error logs
    """
    
    print(checklist)

def main():
    """Main execution"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         BRAIN LINK TRACKER - PRE-DEPLOYMENT CHECK        ║
    ║                    October 22, 2025                      ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    results = {
        'env_vars': check_env_variables(),
        'critical_files': check_critical_files(),
        'code_quality': check_code_quality(),
        'build_files': check_build_files(),
        'package_json': check_package_json(),
        'quantum_redirect': check_quantum_redirect()
    }
    
    generate_checklist()
    
    # Final summary
    print_header("FINAL SUMMARY")
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{check.replace('_', ' ').title()}: {status}")
    
    if all_passed:
        print("\n" + "="*60)
        print("  ✓ ALL CHECKS PASSED - READY FOR DEPLOYMENT")
        print("="*60 + "\n")
        print("  Run: bash DEPLOY_TO_PRODUCTION.sh")
        print("")
        return 0
    else:
        print("\n" + "="*60)
        print("  ✗ SOME CHECKS FAILED - FIX ISSUES BEFORE DEPLOYING")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
