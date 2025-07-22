#!/usr/bin/env python3
"""
Test script to simulate the exact voice assistant booking that's failing
"""

import requests
import json
import sys

# Configuration
base_url = "http://localhost:8001"

def test_voice_booking_api():
    """Test the exact voice assistant booking that's failing"""
    
    print("🔍 Testing Voice Assistant Booking API...")
    print(f"📍 Base URL: {base_url}")
    
    # Step 1: Login as the user from the image
    user_email = "arhumzeenath20103@gmail.com"
    
    print(f"\n🔐 Step 1: Login as user ({user_email})")
    
    try:
        # Request OTP
        login_response = requests.post(f"{base_url}/user/login", json={
            "email": user_email
        })
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return
            
        print("✅ OTP sent successfully")
        
        # For testing, we need to get the OTP from the database
        print("📝 Note: Check backend logs for OTP")
        
    except Exception as e:
        print(f"❌ Login request failed: {e}")
        return
    
    # Step 2: Simulate the exact booking data from the image
    print(f"\n📋 Step 2: Simulate Exact Voice Booking Data")
    
    voice_booking_data = {
        "employee_name": "Sarah Johnson",
        "department": "HR",  # Assuming HR for interview
        "reason": "Interview",
        "appointment_date": "2025-07-16",  # Today's date
        "appointment_time": "15:00",  # 3 PM
        "visitor_name": "Arhum Khan",
        "visitor_email": "arhumzeenath20103@gmail.com",
        "visitor_phone": "9372416957",
        "booking_method": "voice"
    }
    
    print("📋 Voice booking data:")
    print(json.dumps(voice_booking_data, indent=2))
    
    # Step 3: Test appointment creation with a valid token
    print(f"\n🔍 Step 3: Test Appointment Creation")
    print("⚠️  This requires a valid authentication token")
    print("   We need to get the OTP and verify it first")
    
    # For now, let's test the database function directly
    print(f"\n🔍 Step 4: Test Database Function Directly")
    
    try:
        from database import create_appointment
        
        # Test with company_id 1 (from debug info)
        appointment_id = create_appointment(
            employee_name=voice_booking_data["employee_name"],
            department=voice_booking_data["department"],
            reason=voice_booking_data["reason"],
            appointment_date=voice_booking_data["appointment_date"],
            appointment_time=voice_booking_data["appointment_time"],
            visitor_name=voice_booking_data["visitor_name"],
            visitor_email=voice_booking_data["visitor_email"],
            visitor_phone=voice_booking_data["visitor_phone"],
            company_id=1,  # From debug info
            booking_method=voice_booking_data["booking_method"]
        )
        
        if appointment_id:
            print(f"✅ Database function successful! Appointment ID: {appointment_id}")
        else:
            print("❌ Database function failed - returned None")
            
    except Exception as e:
        print(f"❌ Database function error: {e}")
        import traceback
        traceback.print_exc()

def test_api_endpoint_directly():
    """Test the API endpoint directly with the exact data"""
    print(f"\n🔍 Step 5: Test API Endpoint Directly")
    
    # We need a valid token for this test
    print("⚠️  To test the API endpoint directly, we need:")
    print("1. A valid authentication token")
    print("2. The exact request that's failing")
    
    # Let's check what the frontend is actually sending
    print("\n📋 Expected API Request:")
    print("POST /appointments")
    print("Headers: Authorization: Bearer <token>")
    print("Body: The voice_booking_data from above")

if __name__ == "__main__":
    test_voice_booking_api()
    test_api_endpoint_directly()
    
    print("\n" + "=" * 60)
    print("📋 Analysis:")
    print("1. ✅ User authentication works (company_id: 1)")
    print("2. ❌ API call fails with 'Failed to create appointment'")
    print("3. 🔍 Need to check backend logs for the actual error")
    print("4. 🔍 Database function might be working, but API endpoint failing")
    print("\n💡 Next Steps:")
    print("   - Check backend server logs when voice booking is attempted")
    print("   - Look for the actual error in the /appointments POST endpoint")
    print("   - Verify the request format and authentication") 