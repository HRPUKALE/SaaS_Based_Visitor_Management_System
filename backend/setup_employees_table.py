#!/usr/bin/env python3
"""Setup employees table in the database"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_connection

def setup_employees_table():
    """Create the employees table if it doesn't exist"""
    try:
        connection = get_connection()
        if not connection:
            print("❌ Failed to connect to database")
            return False
        
        cursor = connection.cursor()
        
        # Create employees table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            department VARCHAR(100) NOT NULL,
            designation VARCHAR(100),
            phone VARCHAR(15),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
            UNIQUE KEY unique_email_company (email, company_id),
            INDEX idx_company_id (company_id),
            INDEX idx_department (department),
            INDEX idx_email (email),
            INDEX idx_active (is_active)
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        
        print("✅ Employees table created successfully")
        
        # Add some sample employees for testing
        sample_employees = [
            (1, "John Doe", "john@techcorp.com", "IT", "Developer", "+1234567890"),
            (1, "Jane Smith", "jane@techcorp.com", "HR", "Manager", "+1234567891"),
            (1, "Bob Johnson", "bob@techcorp.com", "Sales", "Representative", "+1234567892"),
            (2, "Alice Brown", "alice@innovate.com", "Marketing", "Specialist", "+1234567893"),
            (2, "Charlie Wilson", "charlie@innovate.com", "Finance", "Analyst", "+1234567894"),
        ]
        
        insert_query = """
        INSERT IGNORE INTO employees (company_id, name, email, department, designation, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_query, sample_employees)
        connection.commit()
        
        print(f"✅ Added {len(sample_employees)} sample employees")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up employees table: {e}")
        return False

if __name__ == "__main__":
    print("Setting up employees table...")
    success = setup_employees_table()
    if success:
        print("🎉 Employees table setup completed successfully!")
    else:
        print("💥 Employees table setup failed!")
        sys.exit(1) 