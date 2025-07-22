#!/usr/bin/env python3
"""
Test script for superadmin authentication flow
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_superadmin_flow():
    print("Testing Superadmin Authentication Flow...")
    print("=" * 60)
    
    # Step 1: Superadmin login (send OTP)
    print("1. Sending OTP to superadmin...")
    login_response = requests.post(
        f"{BASE_URL}/superadmin/login",
        json={"email": "superadmin@system.com"},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Login response status: {login_response.status_code}")
    print(f"Login response: {login_response.json()}")
    
    if login_response.status_code != 200:
        print("❌ Login failed!")
        return
    
    # Step 2: Verify OTP (use any 6-digit number for demo)
    print("\n2. Verifying OTP...")
    verify_response = requests.post(
        f"{BASE_URL}/superadmin/verify-otp",
        json={"email": "superadmin@system.com", "otp": "123456"},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Verify response status: {verify_response.status_code}")
    print(f"Verify response: {verify_response.json()}")
    
    if verify_response.status_code != 200:
        print("❌ OTP verification failed!")
        return
    
    # Extract token
    token_data = verify_response.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        print("❌ No access token received!")
        return
    
    print(f"✅ Access token received: {access_token[:20]}...")
    
    # Step 3: Test protected endpoint
    print("\n3. Testing protected endpoint...")
    companies_response = requests.get(
        f"{BASE_URL}/superadmin/companies",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"Companies response status: {companies_response.status_code}")
    print(f"Companies response: {companies_response.json()}")
    
    if companies_response.status_code == 200:
        print("✅ Authentication successful!")
    else:
        print("❌ Authentication failed!")
    
    print("=" * 60)

if __name__ == "__main__":
    test_superadmin_flow() 