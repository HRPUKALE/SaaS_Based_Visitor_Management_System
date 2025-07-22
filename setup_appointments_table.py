#!/usr/bin/env python3
"""
Script to create the appointments table in the database
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import get_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_appointments_table():
    """Create the appointments table"""
    try:
        connection = get_connection()
        if not connection:
            logger.error("Failed to connect to database")
            return False
        
        cursor = connection.cursor()
        
        # Create appointments table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_name VARCHAR(255) NOT NULL,
            department VARCHAR(255) NOT NULL,
            reason TEXT,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            visitor_name VARCHAR(255) NOT NULL,
            visitor_email VARCHAR(255) NOT NULL,
            visitor_phone VARCHAR(50),
            company_id INT NOT NULL,
            booking_method ENUM('manual', 'voice') NOT NULL DEFAULT 'manual',
            status ENUM('confirmed', 'cancelled', 'completed', 'rescheduled') DEFAULT 'confirmed',
            qr_code_sent BOOLEAN DEFAULT FALSE,
            email_sent BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
            INDEX idx_visitor_email (visitor_email),
            INDEX idx_appointment_date (appointment_date),
            INDEX idx_company_id (company_id),
            INDEX idx_status (status),
            INDEX idx_booking_method (booking_method),
            INDEX idx_employee_name (employee_name),
            INDEX idx_department (department)
        );
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        
        logger.info("Appointments table created successfully!")
        
        # Verify the table was created
        cursor.execute("SHOW TABLES LIKE 'appointments'")
        result = cursor.fetchone()
        
        if result:
            logger.info("Appointments table verification: SUCCESS")
            
            # Show table structure
            cursor.execute("DESCRIBE appointments")
            columns = cursor.fetchall()
            logger.info("Table structure:")
            for column in columns:
                logger.info(f"  {column[0]} - {column[1]}")
        else:
            logger.error("Appointments table verification: FAILED")
            return False
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creating appointments table: {e}")
        return False

if __name__ == "__main__":
    print("Creating appointments table...")
    success = create_appointments_table()
    
    if success:
        print("✅ Appointments table created successfully!")
    else:
        print("❌ Failed to create appointments table")
        sys.exit(1) 