#!/usr/bin/env python3
"""
Test script to debug the appointments endpoint 500 error
"""

import requests
import json
import sys

# Configuration
base_url = "http://localhost:8001"

def test_appointments_endpoint():
    """Test the appointments endpoint with proper authentication"""
    
    print("🔍 Testing Appointments Endpoint...")
    print(f"📍 Base URL: {base_url}")
    
    # Step 1: Test if server is running
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Server is running (Health check: {health_response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on port 8001")
        print("💡 Please start the backend server with: python start_server.py")
        return
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Step 2: Login as admin to get token
    admin_email = "admin@techcorp.com"  # Use existing admin from schema
    
    print(f"\n🔐 Logging in as admin: {admin_email}")
    
    try:
        # Step 2a: Request OTP
        login_response = requests.post(f"{base_url}/admin/login", json={
            "email": admin_email
        })
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return
            
        print("✅ OTP sent successfully")
        
        # Step 2b: For testing, we need to get the OTP from the database
        # Let's use a simple approach - try with a known OTP or get it from logs
        print("📝 Note: You'll need to check the backend logs for the OTP")
        print("   Or use the test_admin_login.py script to get the OTP")
        
        # For now, let's test without authentication to see the error
        print("\n🔍 Testing appointments endpoint without authentication...")
        
        appointments_response = requests.get(f"{base_url}/appointments")
        print(f"Appointments response (no auth): {appointments_response.status_code}")
        
        if appointments_response.status_code == 401:
            print("✅ Endpoint exists but requires authentication (expected)")
        elif appointments_response.status_code == 500:
            print(f"❌ 500 error even without auth: {appointments_response.text}")
        else:
            print(f"Unexpected response: {appointments_response.status_code} - {appointments_response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_database_connection():
    """Test database connection directly"""
    print("\n🔍 Testing Database Connection...")
    
    try:
        from database import get_connection, get_appointments_by_company
        
        # Test connection
        connection = get_connection()
        if connection:
            print("✅ Database connection successful")
            
            # Test appointments query
            appointments = get_appointments_by_company(1)  # Test with company_id 1
            print(f"✅ Database query successful, found {len(appointments)} appointments")
            
            if appointments:
                print("📋 Sample appointment:")
                print(json.dumps(appointments[0], indent=2, default=str))
                
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Appointments Endpoint Debug Test")
    print("=" * 50)
    
    test_database_connection()
    test_appointments_endpoint()
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. If database test fails, check MySQL connection")
    print("2. If server is not running, start with: python start_server.py")
    print("3. If 500 error persists, check backend logs for detailed error")
    print("4. Use test_admin_login.py to get a valid token for testing") 