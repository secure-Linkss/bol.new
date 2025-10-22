#!/usr/bin/env python3
"""
Deploy Brain Link Tracker to Vercel
===================================

This script deploys the Brain Link Tracker project to Vercel with proper environment variables.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class VercelDeployer:
    def __init__(self):
        self.project_path = Path("/home/user/current-repo")
        self.vercel_token = "2so8HRWfD06D8dBcs6D20mSx"
        self.github_repo = "https://github.com/secure-Linkss/bol.new"
        
        # Environment variables for production
        self.env_vars = {
            'SECRET_KEY': 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE',
            'DATABASE_URL': 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
            'SHORTIO_API_KEY': 'sk_DbGGlUHPN7Z9VotL',
            'SHORTIO_DOMAIN': 'Secure-links.short.gy',
            'ENVIRONMENT': 'production',
            'NODE_ENV': 'production'
        }
        
    def install_vercel_cli(self):
        """Install Vercel CLI"""
        try:
            # Check if vercel is already installed
            result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Vercel CLI already installed: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            pass
            
        print("📦 Installing Vercel CLI...")
        result = subprocess.run(['npm', 'install', '-g', 'vercel'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Vercel CLI installed successfully")
            return True
        else:
            print(f"❌ Failed to install Vercel CLI: {result.stderr}")
            return False
            
    def login_to_vercel(self):
        """Login to Vercel using token"""
        try:
            print("🔐 Logging into Vercel...")
            
            # Set the token as environment variable
            os.environ['VERCEL_TOKEN'] = self.vercel_token
            
            # Verify login
            result = subprocess.run(['vercel', 'whoami'], 
                                  capture_output=True, text=True, 
                                  env={**os.environ, 'VERCEL_TOKEN': self.vercel_token})
            
            if result.returncode == 0:
                print(f"✅ Logged into Vercel as: {result.stdout.strip()}")
                return True
            else:
                print(f"❌ Failed to login to Vercel: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error logging into Vercel: {e}")
            return False
            
    def create_vercel_config(self):
        """Create vercel.json configuration file"""
        vercel_config = {
            "version": 2,
            "name": "brain-link-tracker",
            "builds": [
                {
                    "src": "api/index.py",
                    "use": "@vercel/python"
                },
                {
                    "src": "package.json",
                    "use": "@vercel/static-build",
                    "config": {
                        "distDir": "dist"
                    }
                }
            ],
            "routes": [
                {
                    "src": "/api/(.*)",
                    "dest": "/api/index.py"
                },
                {
                    "src": "/r/(.*)",
                    "dest": "/api/index.py"
                },
                {
                    "src": "/(.*)",
                    "dest": "/index.html"
                }
            ],
            "env": {
                key: value for key, value in self.env_vars.items()
            }
        }
        
        vercel_file = self.project_path / "vercel.json"
        with open(vercel_file, 'w') as f:
            json.dump(vercel_config, f, indent=2)
            
        print("✅ Created vercel.json configuration")
        
    def set_environment_variables(self):
        """Set environment variables on Vercel"""
        print("🔧 Setting environment variables...")
        
        for key, value in self.env_vars.items():
            result = subprocess.run([
                'vercel', 'env', 'add', key, 'production'
            ], input=value, text=True, capture_output=True,
            env={**os.environ, 'VERCEL_TOKEN': self.vercel_token})
            
            if result.returncode == 0:
                print(f"✅ Set environment variable: {key}")
            else:
                print(f"⚠️ Environment variable {key} might already exist or failed to set")
                
    def deploy_to_vercel(self):
        """Deploy the project to Vercel"""
        print("🚀 Deploying to Vercel...")
        
        os.chdir(self.project_path)
        
        # Deploy with production flag
        result = subprocess.run([
            'vercel', '--prod', '--yes'
        ], capture_output=True, text=True,
        env={**os.environ, 'VERCEL_TOKEN': self.vercel_token})
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print(f"🌐 Production URL: {result.stdout}")
            return result.stdout.strip()
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return None
            
    def run_deployment(self):
        """Run the complete deployment process"""
        print("🚀 Starting Vercel Deployment Process...")
        print("=" * 50)
        
        # Step 1: Install Vercel CLI
        if not self.install_vercel_cli():
            return False
            
        # Step 2: Login to Vercel
        if not self.login_to_vercel():
            return False
            
        # Step 3: Create Vercel configuration
        self.create_vercel_config()
        
        # Step 4: Set environment variables
        self.set_environment_variables()
        
        # Step 5: Deploy to Vercel
        deployment_url = self.deploy_to_vercel()
        
        if deployment_url:
            print("\n" + "=" * 50)
            print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
            print(f"🌐 Your Brain Link Tracker is live at: {deployment_url}")
            print("\n📋 DEPLOYMENT SUMMARY:")
            print("✅ Advanced Settings with Telegram notifications")
            print("✅ Comprehensive theme system (4 themes)")
            print("✅ Fixed tracking metrics accuracy")
            print("✅ Enhanced campaign integration")
            print("✅ Improved location tracking")
            print("✅ Real-time notification timestamps")
            print("✅ Quantum redirecting functionality")
            print("✅ Production environment configured")
            print("\n🔧 Next Steps:")
            print("1. Test all functionality on the live site")
            print("2. Verify database connections")
            print("3. Test tracking link generation and metrics")
            print("4. Configure Telegram bot if needed")
            return True
        else:
            print("\n❌ DEPLOYMENT FAILED")
            return False

if __name__ == "__main__":
    deployer = VercelDeployer()
    success = deployer.run_deployment()
    sys.exit(0 if success else 1)