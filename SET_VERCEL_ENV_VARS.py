#!/usr/bin/env python3
"""
Set Environment Variables on Vercel Project
"""

import requests
import json
import sys

VERCEL_TOKEN = "2so8HRWfD06D8dBcs6D20mSx"

# Read project ID from .vercel/project.json
try:
    with open('.vercel/project.json', 'r') as f:
        vercel_config = json.load(f)
        PROJECT_ID = vercel_config.get('projectId')
        print(f"Project ID: {PROJECT_ID}")
except Exception as e:
    print(f"Error reading project ID: {e}")
    sys.exit(1)

# Environment variables - ALL OF THEM
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

def get_existing_env_vars(project_id):
    """Get existing environment variables"""
    url = f"https://api.vercel.com/v9/projects/{project_id}/env"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get('envs', [])
    return []

def delete_env_var(project_id, env_id):
    """Delete an environment variable"""
    url = f"https://api.vercel.com/v9/projects/{project_id}/env/{env_id}"
    response = requests.delete(url, headers=HEADERS)
    return response.status_code in [200, 204]

def create_env_var(project_id, key, value):
    """Create a new environment variable"""
    url = f"https://api.vercel.com/v10/projects/{project_id}/env"
    data = {
        "key": key,
        "value": value,
        "target": ["production", "preview", "development"],
        "type": "encrypted"
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code in [200, 201], response

def main():
    print("\n" + "="*80)
    print("SETTING VERCEL ENVIRONMENT VARIABLES")
    print("="*80)
    
    if not PROJECT_ID:
        print("❌ No project ID found")
        return 1
    
    # Get existing environment variables
    print("\nChecking existing environment variables...")
    existing_vars = get_existing_env_vars(PROJECT_ID)
    existing_keys = {env['key']: env['id'] for env in existing_vars}
    
    print(f"Found {len(existing_vars)} existing variables")
    
    # Delete existing variables that we're about to recreate
    for key in ENV_VARS.keys():
        if key in existing_keys:
            print(f"Deleting existing {key}...")
            delete_env_var(PROJECT_ID, existing_keys[key])
    
    # Create all environment variables
    print("\nCreating environment variables...")
    success_count = 0
    failed = []
    
    for key, value in ENV_VARS.items():
        success, response = create_env_var(PROJECT_ID, key, value)
        
        if success:
            print(f"✅ {key}")
            success_count += 1
        else:
            print(f"❌ {key}: {response.status_code} - {response.text}")
            failed.append(key)
    
    print("\n" + "="*80)
    print(f"✅ Successfully configured {success_count}/{len(ENV_VARS)} environment variables")
    
    if failed:
        print(f"❌ Failed to configure: {', '.join(failed)}")
        return 1
    
    print("\n🎉 All environment variables configured successfully!")
    print("="*80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
