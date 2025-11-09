#!/usr/bin/env python3
"""
Debug Runtime Issues
Start the Flask backend and test API endpoints that the frontend depends on
"""

import os
import sys
import time
import requests
import subprocess
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RuntimeDebugger:
    def __init__(self):
        self.backend_process = None
        self.base_url = "http://localhost:5000"
        
    def start_backend(self):
        """Start Flask backend"""
        print("🔧 Starting Flask backend...")
        
        try:
            env = os.environ.copy()
            self.backend_process = subprocess.Popen(
                [sys.executable, 'api/index.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Wait for startup
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Backend started successfully")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Backend failed to start:")
                print(f"STDOUT: {stdout.decode()[:500]}")
                print(f"STDERR: {stderr.decode()[:500]}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {str(e)}")
            return False
    
    def test_critical_endpoints(self):
        """Test API endpoints that frontend depends on"""
        print("\\n🔍 Testing critical API endpoints...")
        
        # Critical endpoints that Layout.jsx calls
        endpoints = [
            ('/api/auth/me', 'User profile endpoint'),
            ('/api/auth/validate', 'Token validation endpoint'),
            ('/api/auth/status', 'Auth status endpoint'),
            ('/api/analytics/overview', 'Analytics overview'),
        ]
        
        results = []
        for endpoint, description in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                status = response.status_code
                
                if status in [200, 401, 403]:  # These are acceptable
                    print(f"✅ {description}: HTTP {status}")
                    results.append(True)
                elif status == 404:
                    print(f"❌ {description}: HTTP {status} - Endpoint not found")
                    results.append(False)
                else:
                    print(f"⚠️  {description}: HTTP {status}")
                    results.append(True)  # Might be OK
                    
            except requests.exceptions.ConnectionError:
                print(f"❌ {description}: Connection failed")
                results.append(False)
            except Exception as e:
                print(f"❌ {description}: {str(e)}")
                results.append(False)
        
        return all(results)
    
    def test_static_serving(self):
        """Test if static files are served correctly"""
        print("\\n🔍 Testing static file serving...")
        
        try:
            # Test main page
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                print("✅ Main page serves correctly")
                
                content = response.text
                if 'root' in content:
                    print("✅ Root div found in served HTML")
                else:
                    print("❌ Root div not found in served HTML")
                    
                if 'script' in content:
                    print("✅ Script tags found in served HTML")
                else:
                    print("❌ No script tags in served HTML")
                    
                return True
            else:
                print(f"❌ Main page returns HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Static serving test failed: {str(e)}")
            return False
    
    def check_environment_in_runtime(self):
        """Check if environment variables are accessible in runtime"""
        print("\\n🔍 Checking runtime environment...")
        
        required_vars = ['DATABASE_URL', 'SECRET_KEY']
        for var in required_vars:
            if os.getenv(var):
                print(f"✅ {var}: Available")
            else:
                print(f"❌ {var}: Missing")
    
    def cleanup(self):
        """Clean up processes"""
        if self.backend_process:
            print("\\n🧹 Stopping backend...")
            self.backend_process.terminate()
            self.backend_process.wait()
    
    def run_debug_session(self):
        """Run complete debugging session"""
        print("🐛 Runtime Debugging Session")
        print("=" * 50)
        
        self.check_environment_in_runtime()
        
        if not self.start_backend():
            print("❌ Cannot continue without backend")
            return False
        
        try:
            # Wait a bit more for backend to fully start
            time.sleep(2)
            
            # Run tests
            static_ok = self.test_static_serving()
            api_ok = self.test_critical_endpoints()
            
            print("\\n" + "=" * 50)
            print("📊 DEBUG SUMMARY")
            print("=" * 50)
            
            if static_ok and api_ok:
                print("🎉 Backend appears to be working correctly!")
                print("🔍 The white screen issue might be:")
                print("   1. Frontend JavaScript runtime errors")
                print("   2. CORS issues between frontend and backend")
                print("   3. Missing environment variables on Vercel")
                print("   4. Build artifacts not being served correctly")
            else:
                print("❌ Backend issues detected:")
                if not static_ok:
                    print("   - Static file serving problems")
                if not api_ok:
                    print("   - API endpoint issues")
            
            return static_ok and api_ok
            
        finally:
            self.cleanup()

if __name__ == "__main__":
    debugger = RuntimeDebugger()
    success = debugger.run_debug_session()
    sys.exit(0 if success else 1)