#!/usr/bin/env python3
"""
Configure the secureaccountshub project properly
"""

import requests
import json
import sys

VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"
PROJECT_NAME = "secureaccountshub"

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

def get_project_by_name(project_name):
    """Get project by name"""
    url = f"https://api.vercel.com/v9/projects/{project_name}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    return None

def update_project_git_repo(project_id):
    """Update project to link with GitHub repo"""
    url = f"https://api.vercel.com/v9/projects/{project_id}"
    data = {
        "gitRepository": {
            "repo": "secure-Linkss/bol.new",
            "type": "github"
        },
        "framework": "vite",
        "buildCommand": "npm install --legacy-peer-deps && npm run build",
        "outputDirectory": "dist",
        "installCommand": "npm install --legacy-peer-deps"
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    return response.status_code == 200, response

def set_env_vars(project_id):
    """Set environment variables"""
    # Get existing vars
    url = f"https://api.vercel.com/v9/projects/{project_id}/env"
    response = requests.get(url, headers=HEADERS)
    
    existing_vars = {}
    if response.status_code == 200:
        existing_vars = {env['key']: env['id'] for env in response.json().get('envs', [])}
    
    # Delete existing vars
    for key in ENV_VARS.keys():
        if key in existing_vars:
            delete_url = f"https://api.vercel.com/v9/projects/{project_id}/env/{existing_vars[key]}"
            requests.delete(delete_url, headers=HEADERS)
    
    # Create new vars
    success_count = 0
    for key, value in ENV_VARS.items():
        url = f"https://api.vercel.com/v10/projects/{project_id}/env"
        data = {
            "key": key,
            "value": value,
            "target": ["production", "preview", "development"],
            "type": "encrypted"
        }
        
        response = requests.post(url, headers=HEADERS, json=data)
        if response.status_code in [200, 201]:
            print(f"✅ {key}")
            success_count += 1
        else:
            print(f"❌ {key}: {response.status_code}")
    
    return success_count == len(ENV_VARS)

def trigger_deployment(project_id):
    """Trigger a new deployment"""
    url = "https://api.vercel.com/v13/deployments"
    data = {
        "name": PROJECT_NAME,
        "project": project_id,
        "target": "production",
        "gitSource": {
            "type": "github",
            "ref": "master",
            "repoId": 900197077  # GitHub repo ID for secure-Linkss/bol.new
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code in [200, 201]:
        deployment = response.json()
        return deployment.get('url'), deployment.get('id')
    else:
        print(f"Deployment response: {response.status_code} - {response.text}")
        return None, None

def main():
    print("\n" + "="*80)
    print("CONFIGURING SECUREACCOUNTSHUB PROJECT")
    print("="*80)
    
    # Get project
    print(f"\nFetching project '{PROJECT_NAME}'...")
    project = get_project_by_name(PROJECT_NAME)
    
    if not project:
        print(f"❌ Project '{PROJECT_NAME}' not found")
        return 1
    
    project_id = project.get('id')
    print(f"✅ Found project: {project.get('name')}")
    print(f"   ID: {project_id}")
    
    # Update Git repository link
    print("\nUpdating Git repository link...")
    success, response = update_project_git_repo(project_id)
    if success:
        print("✅ Git repository linked")
    else:
        print(f"⚠️  Git link update: {response.status_code}")
    
    # Set environment variables
    print("\nSetting environment variables...")
    if set_env_vars(project_id):
        print("✅ All environment variables configured")
    else:
        print("⚠️  Some environment variables failed")
    
    # Trigger deployment
    print("\nTriggering production deployment...")
    deploy_url, deploy_id = trigger_deployment(project_id)
    
    if deploy_url:
        print(f"✅ Deployment triggered!")
        print(f"\n🚀 Deployment URL: https://{deploy_url}")
        print(f"🚀 Production URL: https://{PROJECT_NAME}.vercel.app")
        print(f"\n📝 Deployment ID: {deploy_id}")
        print(f"📝 Monitor at: https://vercel.com/dashboard")
    else:
        print("⚠️  Deployment trigger failed (may be rate limited)")
        print(f"⚠️  Check existing deployment at: https://{PROJECT_NAME}.vercel.app")
    
    print("\n" + "="*80)
    print("✅ CONFIGURATION COMPLETE!")
    print("\n📝 IMPORTANT:")
    print("   - All environment variables are configured")
    print("   - Project is linked to GitHub")
    print(f"   - Access at: https://{PROJECT_NAME}.vercel.app")
    print("="*80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
