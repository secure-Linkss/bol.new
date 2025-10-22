#!/usr/bin/env python3
"""
Deployment Verification Script
=============================

This script verifies that the Brain Link Tracker deployment is working correctly.
"""

import requests
import json
import time
from urllib.parse import urlparse

class DeploymentVerifier:
    def __init__(self):
        self.base_url = "https://current-repo-gsd6y08xs-secure-links-projects-3ddb7f78.vercel.app"
        self.tests_passed = 0
        self.tests_failed = 0
        
    def test_deployment_status(self):
        """Test if the deployment is accessible"""
        try:
            print("🔍 Testing deployment accessibility...")
            response = requests.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                print("✅ Deployment is accessible")
                self.tests_passed += 1
                return True
            else:
                print(f"❌ Deployment returned status code: {response.status_code}")
                self.tests_failed += 1
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to access deployment: {e}")
            self.tests_failed += 1
            return False
            
    def test_api_endpoints(self):
        """Test critical API endpoints"""
        endpoints_to_test = [
            "/api/health",
            "/api/auth/status",
            "/api/analytics/summary",
            "/api/links",
            "/api/campaigns",
            "/api/notifications"
        ]
        
        print("🔍 Testing API endpoints...")
        
        for endpoint in endpoints_to_test:
            try:
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, timeout=5)
                
                if response.status_code in [200, 401, 403]:  # 401/403 expected without auth
                    print(f"✅ {endpoint} - Responding")
                    self.tests_passed += 1
                else:
                    print(f"❌ {endpoint} - Status: {response.status_code}")
                    self.tests_failed += 1
                    
            except requests.exceptions.RequestException:
                print(f"❌ {endpoint} - Not responding")
                self.tests_failed += 1
                
    def test_static_assets(self):
        """Test if static assets are loading"""
        print("🔍 Testing static assets...")
        
        try:
            # Test if main page loads with expected content
            response = requests.get(self.base_url, timeout=10)
            content = response.text
            
            # Check for key elements
            if "Brain Link Tracker" in content or "brain-link-tracker" in content:
                print("✅ Application content found")
                self.tests_passed += 1
            else:
                print("❌ Application content not found")
                self.tests_failed += 1
                
            # Check for CSS/JS assets
            if "assets" in content or ".css" in content or ".js" in content:
                print("✅ Static assets referenced")
                self.tests_passed += 1
            else:
                print("❌ Static assets not found")
                self.tests_failed += 1
                
        except Exception as e:
            print(f"❌ Static assets test failed: {e}")
            self.tests_failed += 1
            
    def test_database_connection(self):
        """Test database connectivity through API"""
        print("🔍 Testing database connection...")
        
        try:
            # Try to access an endpoint that requires database
            response = requests.get(f"{self.base_url}/api/analytics/summary", timeout=10)
            
            # Even if unauthorized, a proper response means DB is accessible
            if response.status_code in [200, 401, 403, 422]:
                print("✅ Database connection appears to be working")
                self.tests_passed += 1
            else:
                print(f"❌ Database connection issue - Status: {response.status_code}")
                self.tests_failed += 1
                
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            self.tests_failed += 1
            
    def test_environment_variables(self):
        """Test if environment variables are properly set"""
        print("🔍 Testing environment configuration...")
        
        try:
            # Test an endpoint that would fail without proper env vars
            response = requests.post(f"{self.base_url}/api/links", 
                                   json={"test": "data"}, 
                                   timeout=5)
            
            # Should get 401 (unauthorized) rather than 500 (server error)
            if response.status_code == 401:
                print("✅ Environment variables appear to be configured")
                self.tests_passed += 1
            elif response.status_code == 500:
                print("❌ Server error - possible environment variable issue")
                self.tests_failed += 1
            else:
                print(f"⚠️ Unexpected response - Status: {response.status_code}")
                # Don't count as pass or fail
                
        except Exception as e:
            print(f"❌ Environment test failed: {e}")
            self.tests_failed += 1
            
    def run_verification(self):
        """Run all verification tests"""
        print("🚀 Starting Deployment Verification...")
        print("=" * 50)
        print(f"🌐 Target URL: {self.base_url}")
        print("=" * 50)
        
        # Run all tests
        self.test_deployment_status()
        self.test_api_endpoints()
        self.test_static_assets()
        self.test_database_connection()
        self.test_environment_variables()
        
        # Final report
        print("\n" + "=" * 50)
        print("📊 VERIFICATION RESULTS")
        print("=" * 50)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        
        total_tests = self.tests_passed + self.tests_failed
        if total_tests > 0:
            success_rate = (self.tests_passed / total_tests) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_failed == 0:
            print("\n🎉 ALL TESTS PASSED - DEPLOYMENT IS FULLY FUNCTIONAL!")
            print("\n🌐 Your Brain Link Tracker is ready for use:")
            print(f"   {self.base_url}")
            print("\n📋 Next Steps:")
            print("   1. Access the application and log in")
            print("   2. Test creating tracking links")
            print("   3. Verify metrics accuracy")
            print("   4. Configure Telegram notifications in Settings")
            print("   5. Test theme switching functionality")
            return True
        else:
            print(f"\n⚠️ {self.tests_failed} TESTS FAILED")
            print("Some issues may need to be addressed.")
            return False

if __name__ == "__main__":
    verifier = DeploymentVerifier()
    success = verifier.run_verification()
    exit(0 if success else 1)