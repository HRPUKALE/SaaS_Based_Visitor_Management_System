#!/usr/bin/env python3
"""
Simple test to isolate appointment creation issue
"""

import requests
import json

# Configuration
base_url = "http://localhost:8001"

def test_simple_appointment_creation():
    """Test appointment creation with minimal data"""
    
    print("🔍 Testing Simple Appointment Creation...")
    
    # Test data
    test_appointment = {
        "employee_name": "Test Employee",
        "department": "Test Department",
        "reason": "Test appointment",
        "appointment_date": "2025-07-16",
        "appointment_time": "10:00",
        "visitor_name": "Test Visitor",
        "visitor_email": "test@example.com",
        "visitor_phone": "1234567890",
        "booking_method": "voice"
    }
    
    print("📋 Test appointment data:")
    print(json.dumps(test_appointment, indent=2))
    
    # Test database function directly
    print("\n🔍 Testing Database Function Directly...")
    
    try:
        from database import create_appointment, get_appointment_by_id
        
        # Create appointment
        appointment_id = create_appointment(
            employee_name=test_appointment["employee_name"],
            department=test_appointment["department"],
            reason=test_appointment["reason"],
            appointment_date=test_appointment["appointment_date"],
            appointment_time=test_appointment["appointment_time"],
            visitor_name=test_appointment["visitor_name"],
            visitor_email=test_appointment["visitor_email"],
            visitor_phone=test_appointment["visitor_phone"],
            company_id=1,
            booking_method=test_appointment["booking_method"]
        )
        
        if appointment_id:
            print(f"✅ Database function successful! Appointment ID: {appointment_id}")
            
            # Test retrieving the appointment
            appointment_data = get_appointment_by_id(appointment_id)
            if appointment_data:
                print("✅ Appointment retrieved successfully!")
                print(f"📋 Appointment data: {appointment_data}")
                
                # Test AppointmentResponse creation
                print("\n🔍 Testing AppointmentResponse Creation...")
                try:
                    from models import AppointmentResponse
                    
                    # Convert date and time to string if needed
                    if "appointment_date" in appointment_data and not isinstance(appointment_data["appointment_date"], str):
                        appointment_data["appointment_date"] = str(appointment_data["appointment_date"])
                    if "appointment_time" in appointment_data and not isinstance(appointment_data["appointment_time"], str):
                        appointment_data["appointment_time"] = str(appointment_data["appointment_time"])
                    
                    response = AppointmentResponse(**appointment_data)
                    print("✅ AppointmentResponse created successfully!")
                    print(f"📋 Response data: {response.dict()}")
                    
                except Exception as e:
                    print(f"❌ AppointmentResponse creation failed: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("❌ Failed to retrieve appointment")
        else:
            print("❌ Database function failed")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()

def test_email_service():
    """Test email service separately"""
    
    print("\n🔍 Testing Email Service...")
    
    try:
        from email_service import email_service
        
        # Test appointment data
        test_data = {
            "id": 999,
            "employee_name": "Test Employee",
            "department": "Test Department",
            "appointment_date": "2025-07-16",
            "appointment_time": "10:00",
            "visitor_name": "Test Visitor",
            "visitor_email": "test@example.com",
            "company_name": "Test Company"
        }
        
        # Test QR code generation
        print("🔍 Testing QR Code Generation...")
        qr_code = email_service.generate_qr_code(test_data)
        if qr_code:
            print("✅ QR code generated successfully!")
        else:
            print("❌ QR code generation failed")
        
        # Test email sending (should return True if not configured)
        print("🔍 Testing Email Sending...")
        email_sent = email_service.send_appointment_confirmation(test_data)
        print(f"📧 Email service result: {email_sent}")
        
    except Exception as e:
        print(f"❌ Email service test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_appointment_creation()
    test_email_service()
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    print("1. 🔍 Database function should work")
    print("2. 🔍 AppointmentResponse creation might be the issue")
    print("3. 🔍 Email service should not block appointment creation")
    print("4. 🔍 Check the detailed error logs in the backend") 