#!/usr/bin/env python3
"""
Check Vercel Project Status
"""
import requests
import json

VERCEL_TOKEN = "1JIyxuO5vXBTUGJW5YmNy6GF"
headers = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
}

print("Checking Vercel project status...")

# Get all projects
response = requests.get("https://api.vercel.com/v9/projects", headers=headers)
if response.status_code == 200:
    projects = response.json()['projects']
    
    for project in projects:
        if 'bol' in project['name'].lower():
            print(f"\nProject: {project['name']}")
            print(f"ID: {project['id']}")
            print(f"Framework: {project.get('framework', 'N/A')}")
            
            # Check if connected to GitHub
            if 'link' in project:
                print(f"Connected to: {project['link'].get('type', 'N/A')}")
                if 'gitRepository' in project['link']:
                    print(f"Repository: {project['link']['gitRepository'].get('repo', 'N/A')}")
            
            # Get recent deployments
            dep_response = requests.get(
                f"https://api.vercel.com/v6/deployments?projectId={project['id']}&limit=5",
                headers=headers
            )
            
            if dep_response.status_code == 200:
                deployments = dep_response.json()['deployments']
                print(f"\nRecent Deployments ({len(deployments)}):")
                for dep in deployments:
                    print(f"  - {dep['url']}")
                    print(f"    State: {dep['state']}")
                    print(f"    Created: {dep['createdAt']}")
            
            # Check environment variables
            env_response = requests.get(
                f"https://api.vercel.com/v9/projects/{project['id']}/env",
                headers=headers
            )
            
            if env_response.status_code == 200:
                envs = env_response.json().get('envs', [])
                print(f"\nEnvironment Variables ({len(envs)}):")
                for env in envs:
                    print(f"  - {env['key']}: {'*' * 8} (configured)")
            
            # Get production domain
            if 'targets' in project:
                prod_target = project['targets'].get('production', {})
                if 'alias' in prod_target:
                    print(f"\nProduction URL: https://{prod_target['alias'][0]}")
            
            print("\n" + "="*80)
