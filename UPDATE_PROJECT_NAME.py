#!/usr/bin/env python3
"""
Update Vercel Project Name
"""

import requests
import json
import sys

VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"
PROJECT_ID = "prj_zTxHveyLsIYLfAgOGkyldI6Wyo9s"
NEW_NAME = "secureaccountshub"

HEADERS = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
    "Content-Type": "application/json"
}

def update_project_name():
    """Update project name"""
    url = f"https://api.vercel.com/v9/projects/{PROJECT_ID}"
    data = {
        "name": NEW_NAME
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        project_data = response.json()
        print(f"✅ Project name updated to: {project_data.get('name')}")
        return True
    else:
        print(f"❌ Failed to update project name: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def get_project_info():
    """Get project information"""
    url = f"https://api.vercel.com/v9/projects/{PROJECT_ID}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        project_data = response.json()
        print("\n" + "="*80)
        print("PROJECT INFORMATION")
        print("="*80)
        print(f"Name: {project_data.get('name')}")
        print(f"ID: {project_data.get('id')}")
        print(f"Framework: {project_data.get('framework')}")
        
        # Get production URL
        targets = project_data.get('targets', {})
        if 'production' in targets:
            prod_url = targets['production'].get('url')
            if prod_url:
                print(f"Production URL: https://{prod_url}")
        
        # Get latest deployment
        latest_deployments = project_data.get('latestDeployments', [])
        if latest_deployments:
            latest = latest_deployments[0]
            print(f"\nLatest Deployment:")
            print(f"  URL: https://{latest.get('url')}")
            print(f"  State: {latest.get('state')}")
            print(f"  Ready State: {latest.get('readyState')}")
        
        print("="*80)
        return True
    else:
        print(f"❌ Failed to get project info: {response.status_code}")
        return False

def main():
    print("\n" + "="*80)
    print("UPDATING VERCEL PROJECT NAME")
    print("="*80)
    
    # Update project name
    if update_project_name():
        print("\n✅ Project name updated successfully!")
    else:
        print("\n⚠️  Could not update project name (may already exist)")
    
    # Get current project info
    get_project_info()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
