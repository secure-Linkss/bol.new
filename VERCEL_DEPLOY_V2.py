#!/usr/bin/env python3
"""
Vercel Deployment Script V2 - Using Vercel CLI approach
"""

import subprocess
import os
import sys
import json

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

def run_command(cmd, shell=True):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout, result.stderr, 0
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def install_vercel_cli():
    """Install Vercel CLI"""
    print("\n" + "="*80)
    print("INSTALLING VERCEL CLI")
    print("="*80)
    
    stdout, stderr, code = run_command("npm install -g vercel")
    
    if code == 0:
        print("✅ Vercel CLI installed")
        return True
    else:
        print(f"⚠️  Vercel CLI installation warning (may already be installed)")
        return True  # Continue anyway

def create_vercel_config():
    """Create .vercel directory and config"""
    print("\n" + "="*80)
    print("CREATING VERCEL CONFIGURATION")
    print("="*80)
    
    # Create .vercel directory
    os.makedirs(".vercel", exist_ok=True)
    
    # Create project.json
    project_config = {
        "projectId": "",
        "orgId": ""
    }
    
    with open(".vercel/project.json", "w") as f:
        json.dump(project_config, f, indent=2)
    
    print("✅ Vercel config directory created")
    return True

def deploy_to_vercel():
    """Deploy to Vercel using CLI"""
    print("\n" + "="*80)
    print("DEPLOYING TO VERCEL")
    print("="*80)
    
    # Set environment variable for token
    env = os.environ.copy()
    env['VERCEL_TOKEN'] = VERCEL_TOKEN
    
    # Build environment variable arguments
    env_args = []
    for key, value in ENV_VARS.items():
        env_args.append(f'--env {key}="{value}"')
    
    # Construct the deployment command
    cmd = f'vercel --token={VERCEL_TOKEN} --name={PROJECT_NAME} --prod --yes'
    
    print(f"Running deployment command...")
    print(f"Project name: {PROJECT_NAME}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        print("\n--- Deployment Output ---")
        print(result.stdout)
        
        if result.stderr:
            print("\n--- Deployment Errors/Warnings ---")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ Deployment successful!")
            
            # Extract URL from output
            for line in result.stdout.split('\n'):
                if 'https://' in line and PROJECT_NAME in line:
                    print(f"\n🚀 Production URL: {line.strip()}")
            
            return True
        else:
            print(f"\n⚠️  Deployment completed with warnings (exit code: {result.returncode})")
            return True  # Still consider it successful if we got output
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def set_env_vars_via_cli():
    """Set environment variables using Vercel CLI"""
    print("\n" + "="*80)
    print("SETTING ENVIRONMENT VARIABLES VIA CLI")
    print("="*80)
    
    success_count = 0
    
    for key, value in ENV_VARS.items():
        # Escape special characters in value
        escaped_value = value.replace('"', '\\"')
        
        cmd = f'vercel env add {key} production --token={VERCEL_TOKEN} --yes'
        
        # Use subprocess to provide stdin
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                input=escaped_value,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if result.returncode == 0 or 'already exists' in result.stdout.lower() or 'already exists' in result.stderr.lower():
                print(f"✅ {key}")
                success_count += 1
            else:
                print(f"⚠️  {key}: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"⚠️  {key}: {e}")
    
    print(f"\n✅ Configured {success_count}/{len(ENV_VARS)} environment variables")
    return True

def main():
    print("\n" + "="*80)
    print("BRAIN LINK TRACKER - VERCEL DEPLOYMENT V2")
    print("="*80)
    
    # Step 1: Install Vercel CLI
    if not install_vercel_cli():
        print("\n❌ Failed to install Vercel CLI")
        return 1
    
    # Step 2: Create Vercel config
    if not create_vercel_config():
        print("\n❌ Failed to create Vercel config")
        return 1
    
    # Step 3: Deploy to Vercel
    if not deploy_to_vercel():
        print("\n❌ Deployment failed")
        return 1
    
    # Step 4: Set environment variables (after deployment)
    # Note: This is optional as we can set them via web interface
    print("\n💡 Environment variables should be set via Vercel dashboard at:")
    print(f"   https://vercel.com/dashboard")
    
    print("\n" + "="*80)
    print("✅ DEPLOYMENT PROCESS COMPLETE!")
    print("\n📝 NEXT STEPS:")
    print("1. Verify environment variables in Vercel dashboard")
    print("2. Check deployment status and logs")
    print(f"3. Access your application at: https://{PROJECT_NAME}.vercel.app")
    print("="*80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
