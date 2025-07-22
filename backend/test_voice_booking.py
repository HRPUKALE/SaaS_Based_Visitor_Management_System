#!/usr/bin/env python3
"""
Test script to verify voice assistant booking functionality
"""

import requests
import json
import sys

# Configuration
base_url = "http://localhost:8001"

def test_voice_booking():
    """Test voice assistant booking flow"""
    
    print("🔍 Testing Voice Assistant Booking Flow...")
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
    admin_email = "harshadpukale131@gmail.com"  # Use existing admin
    
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
        print("📝 Note: You'll need to check the backend logs for the OTP")
        print("   Or use the test_admin_login.py script to get the OTP")
        
        # For now, let's test the appointment creation directly with a valid token
        print("\n🔍 Testing appointment creation with voice booking method...")
        
        # Simulate voice assistant booking data
        voice_booking_data = {
            "employee_name": "Test Employee",
            "department": "Test Department", 
            "reason": "Voice assistant test booking",
            "appointment_date": "2024-01-20",
            "appointment_time": "14:00",
            "visitor_name": "Voice Test Visitor",
            "visitor_email": "voice.test@example.com",
            "visitor_phone": "9876543210",
            "booking_method": "voice"
        }
        
        print("📋 Voice booking data:")
        print(json.dumps(voice_booking_data, indent=2))
        
        # We need a valid token to test this
        print("\n⚠️  To test voice booking, you need to:")
        print("1. Run test_admin_login.py to get a valid token")
        print("2. Use that token to test appointment creation")
        print("3. Check if the appointment is saved with booking_method='voice'")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_database_for_voice_bookings():
    """Check database for existing voice bookings"""
    print("\n🔍 Checking Database for Voice Bookings...")
    
    try:
        from database import get_connection
        
        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Check for voice bookings
            query = """
                SELECT * FROM appointments 
                WHERE booking_method = 'voice' 
                ORDER BY created_at DESC
            """
            cursor.execute(query)
            voice_bookings = cursor.fetchall()
            
            print(f"✅ Found {len(voice_bookings)} voice bookings in database")
            
            if voice_bookings:
                print("\n📋 Voice bookings found:")
                for i, booking in enumerate(voice_bookings):
                    print(f"\n--- Voice Booking {i+1} ---")
                    print(f"ID: {booking['id']}")
                    print(f"Employee: {booking['employee_name']}")
                    print(f"Department: {booking['department']}")
                    print(f"Visitor: {booking['visitor_name']}")
                    print(f"Email: {booking['visitor_email']}")
                    print(f"Date: {booking['appointment_date']}")
                    print(f"Time: {booking['appointment_time']}")
                    print(f"Booking Method: {booking['booking_method']}")
                    print(f"Company ID: {booking['company_id']}")
                    print(f"Created: {booking['created_at']}")
            else:
                print("❌ No voice bookings found in database")
                print("💡 This suggests voice assistant bookings are not being saved")
            
            cursor.close()
            connection.close()
            
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Voice Assistant Booking Test")
    print("=" * 50)
    
    test_database_for_voice_bookings()
    test_voice_booking()
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("1. Check if voice bookings exist in database")
    print("2. If none found, voice assistant may not be saving appointments")
    print("3. Verify user authentication and company_id in frontend")
    print("4. Check browser console for API errors during voice booking") 