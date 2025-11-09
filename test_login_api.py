#!/usr/bin/env python3
"""
Test Login API on Deployed URL
"""
import requests
import json

# Test all deployment URLs
DEPLOYMENT_URLS = [
    "https://bol-new-ten.vercel.app",
    "https://bol-62dgjgfu0-secure-links-projects-3ddb7f78.vercel.app",
    "https://bol-project-secure-links-projects-3ddb7f78.vercel.app",
    "https://bolnew-secure-links-projects-3ddb7f78.vercel.app"
]

# Login credentials
LOGIN_DATA = {
    "username": "Brain",
    "password": "Mayflower1!!"
}

print("=" * 80)
print("TESTING LOGIN API ON DEPLOYED URLS")
print("=" * 80)

for url in DEPLOYMENT_URLS:
    print(f"\n🌐 Testing: {url}")
    print("-" * 80)
    
    # Test 1: Check if site is accessible
    try:
        response = requests.get(url, timeout=10)
        print(f"✓ Site accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Site not accessible: {str(e)[:100]}")
        continue
    
    # Test 2: Test login API
    login_url = f"{url}/api/auth/login"
    print(f"\n📝 Testing login endpoint: {login_url}")
    
    try:
        response = requests.post(
            login_url,
            json=LOGIN_DATA,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ LOGIN SUCCESSFUL!")
            print(f"  User: {data.get('user', {}).get('username', 'N/A')}")
            print(f"  Role: {data.get('user', {}).get('role', 'N/A')}")
            print(f"  Token: {data.get('token', 'N/A')[:50]}...")
            print(f"\n{'='*80}")
            print(f"🎉 SUCCESS! Login works on this URL:")
            print(f"   {url}")
            print(f"{'='*80}")
            break
        elif response.status_code == 401:
            print(f"✗ Invalid credentials (401)")
            print(f"  Response: {response.text[:200]}")
        elif response.status_code == 500:
            print(f"✗ Server error (500) - likely database connection issue")
            print(f"  Response: {response.text[:200]}")
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print(f"✗ Request timed out")
    except Exception as e:
        print(f"✗ Error: {str(e)[:200]}")

print(f"\n{'='*80}")
print("TEST COMPLETED")
print("="*80)
