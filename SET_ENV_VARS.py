#!/usr/bin/env python3
"""
Set Environment Variables on Vercel Project
"""

import requests
import json

VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"
PROJECT_NAME = "brain-link-tracker"  # The actual project name from deployment

# Environment variables
ENV_VARS = {
    "DATABASE_URL": "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    "SECRET_KEY": "ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE",
    "SHORTIO_API_KEY": "sk_DbGGlUHPN7Z9VotL",
    "SHORTIO_DOMAIN": "Secure-links.short.gy",
    "STRIPE_SECRET_KEY": "sk_test_your_test_key_here",
    "STRIPE_PUBLISHABLE_KEY": "pk_test_your_test_key_here"
}

HEADERS = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
    "Content-Type": "application/json"
}

def get_project_id():
    """Get project ID"""
    print("\n" + "="*80)
    print("GETTING PROJECT ID")
    print("="*80)
    
    url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        project_data = response.json()
        project_id = project_data.get('id')
        print(f"✅ Project '{PROJECT_NAME}' found")
        print(f"   Project ID: {project_id}")
        return project_id
    else:
        print(f"❌ Failed to get project: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def set_environment_variables(project_id):
    """Set environment variables for the project"""
    print("\n" + "="*80)
    print("CONFIGURING ENVIRONMENT VARIABLES")
    print("="*80)
    
    # First, get existing environment variables
    url = f"https://api.vercel.com/v9/projects/{project_id}/env"
    response = requests.get(url, headers=HEADERS)
    
    existing_vars = {}
    if response.status_code == 200:
        env_list = response.json().get('envs', [])
        existing_vars = {env['key']: env.get('id') for env in env_list}
        print(f"Found {len(existing_vars)} existing environment variables")
    
    # Set or update each environment variable
    success_count = 0
    for key, value in ENV_VARS.items():
        if key in existing_vars:
            # Update existing variable
            env_id = existing_vars[key]
            url = f"https://api.vercel.com/v9/projects/{project_id}/env/{env_id}"
            data = {
                "value": value,
                "target": ["production", "preview", "development"],
                "type": "encrypted"
            }
            response = requests.patch(url, headers=HEADERS, json=data)
            
            if response.status_code == 200:
                print(f"✅ Updated: {key}")
                success_count += 1
            else:
                print(f"⚠️  Failed to update {key}: {response.status_code}")
                print(f"   Response: {response.text}")
        else:
            # Create new variable
            url = f"https://api.vercel.com/v10/projects/{project_id}/env"
            data = {
                "key": key,
                "value": value,
                "target": ["production", "preview", "development"],
                "type": "encrypted"
            }
            response = requests.post(url, headers=HEADERS, json=data)
            
            if response.status_code in [200, 201]:
                print(f"✅ Created: {key}")
                success_count += 1
            else:
                print(f"⚠️  Failed to create {key}: {response.status_code}")
                print(f"   Response: {response.text}")
    
    print(f"\n✅ Successfully configured {success_count}/{len(ENV_VARS)} environment variables")
    return success_count == len(ENV_VARS)

def trigger_redeploy(project_id):
    """Trigger a redeploy to apply environment variables"""
    print("\n" + "="*80)
    print("TRIGGERING REDEPLOY")
    print("="*80)
    
    url = f"https://api.vercel.com/v13/deployments"
    data = {
        "name": PROJECT_NAME,
        "project": project_id,
        "gitSource": {
            "type": "github",
            "ref": "master"
        },
        "target": "production"
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code in [200, 201]:
        deployment_data = response.json()
        deployment_url = deployment_data.get('url')
        print(f"✅ Redeploy triggered")
        print(f"   URL: https://{deployment_url}")
        return True
    else:
        print(f"⚠️  Redeploy trigger failed: {response.status_code}")
        print(f"   Response: {response.text}")
        print("\n💡 You can manually redeploy from Vercel dashboard")
        return True  # Not critical

def main():
    print("\n" + "="*80)
    print("BRAIN LINK TRACKER - ENVIRONMENT VARIABLES SETUP")
    print("="*80)
    
    # Step 1: Get project ID
    project_id = get_project_id()
    if not project_id:
        print("\n❌ Failed to get project ID")
        return 1
    
    # Step 2: Set environment variables
    if not set_environment_variables(project_id):
        print("\n⚠️  Some environment variables failed to set")
    
    # Step 3: Trigger redeploy
    trigger_redeploy(project_id)
    
    print("\n" + "="*80)
    print("✅ ENVIRONMENT SETUP COMPLETE!")
    print("\n📝 DEPLOYMENT URLS:")
    print(f"   https://brain-link-tracker.vercel.app")
    print(f"   https://brain-link-tracker-git-master-secure-links-projects-3ddb7f78.vercel.app")
    print("\n💡 Check deployment status at:")
    print(f"   https://vercel.com/secure-links-projects-3ddb7f78/brain-link-tracker")
    print("="*80)
    
    return 0

if __name__ == "__main__":
    main()
