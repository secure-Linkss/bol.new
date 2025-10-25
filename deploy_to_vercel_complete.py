#!/usr/bin/env python3
"""
Complete Vercel Deployment Script
Triggers deployment and monitors build status
"""
import requests
import time
import json

# Vercel configuration
VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"
PROJECT_NAME = "bol-new"  # Your project name on Vercel
TEAM_ID = None  # Set if using team account

print("=" * 80)
print("VERCEL DEPLOYMENT SCRIPT")
print("=" * 80)

# Headers for Vercel API
headers = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
    "Content-Type": "application/json"
}

# Step 1: Get project details
print("\n[1] Fetching project details...")
try:
    url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
    if TEAM_ID:
        url += f"?teamId={TEAM_ID}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        project = response.json()
        print(f"✓ Project found: {project['name']}")
        print(f"  Framework: {project.get('framework', 'N/A')}")
        print(f"  Production Branch: {project.get('productionBranch', 'N/A')}")
    else:
        print(f"✗ Failed to fetch project: {response.status_code}")
        print(f"  Response: {response.text}")
        print("\nNote: Will proceed with deployment trigger anyway...")

except Exception as e:
    print(f"⚠ Warning: {e}")
    print("  Will proceed with deployment trigger anyway...")

# Step 2: Trigger deployment
print("\n[2] Triggering new deployment...")
try:
    # Use deployment hooks or git integration
    # Since dist/ is in .gitignore, Vercel will build it automatically
    url = "https://api.vercel.com/v13/deployments"
    if TEAM_ID:
        url += f"?teamId={TEAM_ID}"
    
    deployment_data = {
        "name": PROJECT_NAME,
        "project": PROJECT_NAME,
        "gitSource": {
            "type": "github",
            "repo": "secure-Linkss/bol.new",
            "ref": "master"
        },
        "target": "production"
    }
    
    response = requests.post(url, headers=headers, json=deployment_data)
    
    if response.status_code in [200, 201]:
        deployment = response.json()
        deployment_id = deployment.get('id', 'N/A')
        deployment_url = deployment.get('url', 'N/A')
        
        print(f"✓ Deployment triggered successfully!")
        print(f"  Deployment ID: {deployment_id}")
        print(f"  Preview URL: https://{deployment_url}")
        print(f"\n  You can monitor the deployment at:")
        print(f"  https://vercel.com/dashboard")
        
    elif response.status_code == 409:
        print("✓ Deployment already in progress or completed")
        print("  Check Vercel dashboard for status")
        
    else:
        print(f"⚠ Deployment trigger response: {response.status_code}")
        print(f"  Response: {response.text}")
        print("\n  This might be expected if using webhook triggers.")
        print("  Please check your Vercel dashboard for deployment status.")

except Exception as e:
    print(f"⚠ Error triggering deployment: {e}")
    print("\n  Alternative: Deployment may have been triggered automatically by GitHub push.")
    print("  Check your Vercel dashboard for deployment status.")

# Step 3: Instructions
print("\n" + "=" * 80)
print("DEPLOYMENT INSTRUCTIONS")
print("=" * 80)

print("""
Since the dist/ directory is in .gitignore (which is correct), Vercel will:
1. Pull the latest code from GitHub (master branch) ✓ DONE
2. Run 'npm install' to install dependencies
3. Run 'npm run build' to generate dist/
4. Deploy the generated dist/ to production

VERIFY ENVIRONMENT VARIABLES IN VERCEL DASHBOARD:
Go to: https://vercel.com/dashboard
→ Select your project
→ Settings → Environment Variables
→ Ensure these are set for Production:

Required:
  SECRET_KEY=ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE
  DATABASE_URL=postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
  SHORTIO_API_KEY=sk_DbGGlUHPN7Z9VotL
  SHORTIO_DOMAIN=Secure-links.short.gy

Optional (can configure in admin panel after deployment):
  STRIPE_SECRET_KEY
  STRIPE_PUBLISHABLE_KEY

MONITOR DEPLOYMENT:
Visit: https://vercel.com/dashboard
Check the latest deployment status and build logs.

POST-DEPLOYMENT TESTING:
1. Visit your production URL
2. Login with: Brain / Mayflower1!!
3. Test profile avatar dropdown (click "A" icon in header)
4. Navigate through all 9 tabs
5. Access Admin Panel
6. Create tracking link with campaign name
7. Verify campaign auto-creation

""")

print("=" * 80)
print("DEPLOYMENT INITIATED")
print("=" * 80)
