#!/usr/bin/env python3
"""
Test database connection and appointment table
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_connection, create_appointment, get_appointment_by_id
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection"""
    try:
        connection = get_connection()
        if connection:
            logger.info("✅ Database connection successful!")
            
            # Test creating a sample appointment
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES LIKE 'appointments'")
            result = cursor.fetchone()
            
            if result:
                logger.info("✅ Appointments table exists!")
                
                # Test appointment creation
                appointment_id = create_appointment(
                    employee_name="Test Employee",
                    department="Test Department",
                    reason="Test appointment",
                    appointment_date="2024-01-15",
                    appointment_time="10:00",
                    visitor_name="Test Visitor",
                    visitor_email="test@example.com",
                    visitor_phone="1234567890",
                    company_id=1,
                    booking_method="manual"
                )
                
                if appointment_id:
                    logger.info(f"✅ Appointment created successfully with ID: {appointment_id}")
                    
                    # Test retrieving the appointment
                    appointment = get_appointment_by_id(appointment_id)
                    if appointment:
                        logger.info("✅ Appointment retrieved successfully!")
                        logger.info(f"   Employee: {appointment['employee_name']}")
                        logger.info(f"   Visitor: {appointment['visitor_name']}")
                    else:
                        logger.error("❌ Failed to retrieve appointment")
                else:
                    logger.error("❌ Failed to create appointment")
            else:
                logger.error("❌ Appointments table does not exist!")
                
            cursor.close()
            connection.close()
        else:
            logger.error("❌ Database connection failed!")
            
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    print("Testing database connection and appointment functionality...")
    test_database_connection() 