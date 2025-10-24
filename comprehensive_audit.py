#!/usr/bin/env python3
"""
Comprehensive Project Audit Script
Analyzes database, API routes, and frontend components
"""
import os
import sys
import json
from pathlib import Path

print("=" * 80)
print("BRAIN LINK TRACKER - COMPREHENSIVE AUDIT")
print("=" * 80)

# 1. Check database connection
print("\n[1] DATABASE CONNECTION CHECK")
print("-" * 80)
try:
    import psycopg2
    db_url = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
    
    # Parse connection string
    parts = db_url.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    host = host_db[0]
    database = host_db[1].split('?')[0]
    
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user_pass[0],
        password=user_pass[1]
    )
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    
    print(f"✓ Database connected successfully")
    print(f"✓ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check for missing critical tables
    table_names = [t[0] for t in tables]
    critical_tables = ['users', 'campaigns', 'links', 'tracking_events', 'notifications', 
                      'audit_logs', 'security_threats', 'support_tickets', 
                      'subscription_verifications', 'security_settings']
    
    missing_tables = [t for t in critical_tables if t not in table_names]
    if missing_tables:
        print(f"\n⚠ MISSING CRITICAL TABLES: {', '.join(missing_tables)}")
    else:
        print(f"\n✓ All critical tables exist")
    
    conn.close()
    
except Exception as e:
    print(f"✗ Database connection failed: {e}")

# 2. Check API routes
print("\n[2] API ROUTES AUDIT")
print("-" * 80)

api_routes_dir = Path("src/routes")
if api_routes_dir.exists():
    route_files = list(api_routes_dir.glob("*.py"))
    print(f"✓ Found {len(route_files)} route files:")
    for rf in sorted(route_files):
        print(f"  - {rf.name}")
else:
    print("✗ Routes directory not found")

# 3. Check frontend components
print("\n[3] FRONTEND COMPONENTS AUDIT")
print("-" * 80)

components_dir = Path("src/components")
if components_dir.exists():
    jsx_files = list(components_dir.glob("*.jsx"))
    print(f"✓ Found {len(jsx_files)} component files:")
    
    critical_components = ['Layout.jsx', 'AdminPanelComplete.jsx', 'Dashboard.jsx', 
                          'TrackingLinks.jsx', 'Campaign.jsx', 'Analytics.jsx']
    
    for comp in critical_components:
        if Path(components_dir / comp).exists():
            print(f"  ✓ {comp}")
        else:
            print(f"  ✗ {comp} MISSING")
else:
    print("✗ Components directory not found")

# 4. Check environment variables
print("\n[4] ENVIRONMENT VARIABLES CHECK")
print("-" * 80)

required_env_vars = [
    'SECRET_KEY',
    'DATABASE_URL',
    'SHORTIO_API_KEY',
    'SHORTIO_DOMAIN',
]

optional_env_vars = [
    'STRIPE_SECRET_KEY',
    'STRIPE_PUBLISHABLE_KEY',
]

print("Required:")
for var in required_env_vars:
    if os.environ.get(var):
        print(f"  ✓ {var} is set")
    else:
        print(f"  ✗ {var} is MISSING")

print("\nOptional:")
for var in optional_env_vars:
    if os.environ.get(var):
        print(f"  ✓ {var} is set")
    else:
        print(f"  - {var} not set")

# 5. Check for build artifacts
print("\n[5] BUILD ARTIFACTS CHECK")
print("-" * 80)

dist_dir = Path("dist")
if dist_dir.exists():
    print(f"✓ dist/ directory exists")
    if (dist_dir / "index.html").exists():
        print(f"  ✓ index.html found")
    else:
        print(f"  ✗ index.html MISSING")
        
    js_files = list(dist_dir.glob("assets/*.js"))
    css_files = list(dist_dir.glob("assets/*.css"))
    print(f"  ✓ {len(js_files)} JS files")
    print(f"  ✓ {len(css_files)} CSS files")
else:
    print("✗ dist/ directory NOT found - frontend needs building")

# 6. Check package.json
print("\n[6] PACKAGE.JSON CHECK")
print("-" * 80)

package_json = Path("package.json")
if package_json.exists():
    with open(package_json) as f:
        pkg = json.load(f)
    print(f"✓ Project: {pkg.get('name', 'Unknown')}")
    print(f"✓ Version: {pkg.get('version', 'Unknown')}")
    
    scripts = pkg.get('scripts', {})
    print(f"\n  Available scripts:")
    for script_name in ['dev', 'build', 'preview']:
        if script_name in scripts:
            print(f"    ✓ {script_name}: {scripts[script_name]}")
        else:
            print(f"    ✗ {script_name} missing")
else:
    print("✗ package.json not found")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
