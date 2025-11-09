#!/usr/bin/env python3
"""
Vercel Deployment Script with Environment Variables
"""

import requests
import json
import time
import sys

VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"
PROJECT_NAME = "secureaccountshub"
GITHUB_REPO = "secure-Linkss/bol.new"

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
    """Get or create Vercel project"""
    print("\n" + "="*80)
    print("CHECKING VERCEL PROJECT")
    print("="*80)
    
    # Check if project exists
    url = f"https://api.vercel.com/v9/projects/{PROJECT_NAME}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        project_data = response.json()
        project_id = project_data.get('id')
        print(f"✅ Project '{PROJECT_NAME}' found")
        print(f"   Project ID: {project_id}")
        return project_id
    
    # Project doesn't exist, create it
    print(f"⚠️  Project '{PROJECT_NAME}' not found, creating...")
    
    url = "https://api.vercel.com/v9/projects"
    data = {
        "name": PROJECT_NAME,
        "framework": "vite",
        "gitRepository": {
            "repo": GITHUB_REPO,
            "type": "github"
        },
        "buildCommand": "npm install --legacy-peer-deps && npm run build",
        "outputDirectory": "dist",
        "installCommand": "npm install --legacy-peer-deps"
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code in [200, 201]:
        project_data = response.json()
        project_id = project_data.get('id')
        print(f"✅ Project '{PROJECT_NAME}' created")
        print(f"   Project ID: {project_id}")
        return project_id
    else:
        print(f"❌ Failed to create project: {response.status_code}")
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
            else:
                print(f"⚠️  Failed to update {key}: {response.status_code}")
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
            else:
                print(f"⚠️  Failed to create {key}: {response.status_code}")
                print(f"   Response: {response.text}")
    
    print("\n✅ Environment variables configured")
    return True

def trigger_deployment(project_id):
    """Trigger a new deployment"""
    print("\n" + "="*80)
    print("TRIGGERING DEPLOYMENT")
    print("="*80)
    
    url = "https://api.vercel.com/v13/deployments"
    data = {
        "name": PROJECT_NAME,
        "project": project_id,
        "gitSource": {
            "type": "github",
            "repo": GITHUB_REPO,
            "ref": "master"
        },
        "target": "production"
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code in [200, 201]:
        deployment_data = response.json()
        deployment_id = deployment_data.get('id')
        deployment_url = deployment_data.get('url')
        
        print(f"✅ Deployment triggered")
        print(f"   Deployment ID: {deployment_id}")
        print(f"   URL: https://{deployment_url}")
        
        return deployment_id, deployment_url
    else:
        print(f"❌ Failed to trigger deployment: {response.status_code}")
        print(f"   Response: {response.text}")
        return None, None

def check_deployment_status(deployment_id):
    """Check deployment status"""
    print("\n" + "="*80)
    print("CHECKING DEPLOYMENT STATUS")
    print("="*80)
    
    url = f"https://api.vercel.com/v13/deployments/{deployment_id}"
    
    max_attempts = 60  # 5 minutes maximum
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            deployment_data = response.json()
            state = deployment_data.get('readyState')
            
            if state == 'READY':
                print(f"\n✅ Deployment completed successfully!")
                print(f"   URL: https://{deployment_data.get('url')}")
                
                # Get production domain
                alias = deployment_data.get('alias', [])
                if alias:
                    print(f"   Production URL: https://{alias[0]}")
                
                return True
            elif state == 'ERROR':
                print(f"\n❌ Deployment failed")
                print(f"   Error: {deployment_data.get('error', {}).get('message', 'Unknown error')}")
                return False
            elif state in ['BUILDING', 'QUEUED', 'INITIALIZING']:
                print(f"⏳ Status: {state} (attempt {attempt + 1}/{max_attempts})")
                time.sleep(5)
                attempt += 1
            else:
                print(f"⚠️  Unknown state: {state}")
                time.sleep(5)
                attempt += 1
        else:
            print(f"❌ Failed to check status: {response.status_code}")
            return False
    
    print("\n⏰ Deployment timeout - check Vercel dashboard for status")
    return False

def main():
    print("\n" + "="*80)
    print("BRAIN LINK TRACKER - VERCEL DEPLOYMENT")
    print("="*80)
    
    # Step 1: Get or create project
    project_id = get_project_id()
    if not project_id:
        print("\n❌ Failed to get project ID")
        return 1
    
    # Step 2: Set environment variables
    if not set_environment_variables(project_id):
        print("\n❌ Failed to set environment variables")
        return 1
    
    # Step 3: Trigger deployment
    deployment_id, deployment_url = trigger_deployment(project_id)
    if not deployment_id:
        print("\n❌ Failed to trigger deployment")
        return 1
    
    # Step 4: Check deployment status
    success = check_deployment_status(deployment_id)
    
    print("\n" + "="*80)
    if success:
        print("✅ DEPLOYMENT COMPLETE!")
        print(f"\n🚀 Your application is live at:")
        print(f"   https://{deployment_url}")
        print(f"   https://{PROJECT_NAME}.vercel.app")
    else:
        print("❌ DEPLOYMENT INCOMPLETE")
        print(f"\nCheck deployment status at:")
        print(f"   https://vercel.com/dashboard")
    print("="*80)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
