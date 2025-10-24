#!/usr/bin/env python3
"""
Comprehensive System Test
Tests all critical endpoints and functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://bolnew-sigma.vercel.app"  # Update if different
# For local testing, use: BASE_URL = "http://localhost:5173"

def test_login():
    """Test admin login"""
    print("
[TEST] Admin Login...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "Brain",
        "password": "Mayflower1!!"
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✓ Login successful")
            return data.get('token')
        else:
            print(f"✗ Login failed: {data.get('error')}")
            return None
    else:
        print(f"✗ Login request failed: {response.status_code}")
        return None

def test_dashboard(token):
    """Test dashboard endpoint"""
    print("
[TEST] Dashboard Stats...")
    response = requests.get(
        f"{BASE_URL}/api/admin/dashboard/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Dashboard stats retrieved")
        print(f"  Total Users: {data.get('total_users', 0)}")
        print(f"  Total Links: {data.get('total_links', 0)}")
        print(f"  Total Clicks: {data.get('total_clicks', 0)}")
        return True
    else:
        print(f"✗ Dashboard request failed: {response.status_code}")
        return False

def test_geographic_data(token):
    """Test geographic distribution"""
    print("
[TEST] Geographic Distribution...")
    response = requests.get(
        f"{BASE_URL}/api/analytics/geographic-distribution",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            countries = data.get('countries', [])
            print(f"✓ Geographic data retrieved: {len(countries)} countries")
            return True
        else:
            print(f"✗ Geographic data failed: {data.get('error')}")
            return False
    else:
        print(f"✗ Geographic request failed: {response.status_code}")
        return False

def test_campaigns(token):
    """Test campaigns endpoint"""
    print("
[TEST] Campaigns...")
    response = requests.get(
        f"{BASE_URL}/api/admin/campaigns",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        campaigns = data.get('campaigns', [])
        print(f"✓ Campaigns retrieved: {len(campaigns)} campaigns")
        return True
    else:
        print(f"✗ Campaigns request failed: {response.status_code}")
        return False

def main():
    print("=" * 60)
    print("BRAIN LINK TRACKER - SYSTEM TEST")
    print("=" * 60)
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    token = test_login()
    
    if token:
        test_dashboard(token)
        test_geographic_data(token)
        test_campaigns(token)
        
        print("
" + "=" * 60)
        print("TEST SUITE COMPLETED")
        print("=" * 60)
    else:
        print("
✗ Tests aborted - login failed")

if __name__ == '__main__':
    main()
