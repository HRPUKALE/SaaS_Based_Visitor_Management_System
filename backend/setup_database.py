#!/usr/bin/env python3
"""
Database setup script for Voice Assistant SaaS
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'port': os.getenv('DB_PORT', '3306'),
    'password': os.getenv('DB_PASSWORD', 'Hrpukale@131'),
    'charset': 'utf8mb4',
    'autocommit': True
}

def setup_database():
    """Set up the database with the new 3-table structure"""
    
    print("🚀 Setting up Voice Assistant SaaS Database...")
    print("=" * 60)
    
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Drop existing database if it exists
            print("🗑️  Dropping existing database...")
            cursor.execute("DROP DATABASE IF EXISTS voice_assistant_saas")
            
            # Create new database
            print("📦 Creating new database...")
            cursor.execute("CREATE DATABASE voice_assistant_saas")
            cursor.execute("USE voice_assistant_saas")
            
            # Create superadmins table
            print("👑 Creating superadmins table...")
            cursor.execute("""
                CREATE TABLE superadmins (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_email (email),
                    INDEX idx_active (is_active)
                )
            """)
            
            # Create companies table
            print("🏢 Creating companies table...")
            cursor.execute("""
                CREATE TABLE companies (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    domain VARCHAR(255),
                    max_users INT DEFAULT 100,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_by INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES superadmins(id),
                    INDEX idx_email (email),
                    INDEX idx_active (is_active),
                    INDEX idx_created_by (created_by)
                )
            """)
            
            # Create users table
            print("👥 Creating users table...")
            cursor.execute("""
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
                    company_id INT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    otp VARCHAR(6),
                    otp_expiry TIMESTAMP NULL,
                    last_login TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_email_company (email, company_id),
                    INDEX idx_email (email),
                    INDEX idx_company_id (company_id),
                    INDEX idx_role (role),
                    INDEX idx_active (is_active),
                    INDEX idx_otp (otp)
                )
            """)
            
            # Create default superadmin
            print("👑 Creating default superadmin...")
            cursor.execute("""
                INSERT INTO superadmins (email, name) VALUES 
                ('superadmin@system.com', 'System Administrator')
            """)
            
            # Add sample data
            print("📝 Adding sample data...")
            
            # Sample companies
            cursor.execute("""
                INSERT INTO companies (name, email, domain, created_by) VALUES 
                ('TechCorp Inc', 'contact@techcorp.com', 'techcorp.com', 1),
                ('Innovate Solutions', 'info@innovate.com', 'innovate.com', 1)
            """)
            
            # Get the company IDs that were just created
            cursor.execute("SELECT id FROM companies WHERE email IN ('contact@techcorp.com', 'info@innovate.com') ORDER BY email")
            company_ids = cursor.fetchall()
            
            if len(company_ids) >= 2:
                techcorp_id = company_ids[0][0]  # First company (TechCorp)
                innovate_id = company_ids[1][0]  # Second company (Innovate)
                
                # Sample users for TechCorp
                cursor.execute("""
                    INSERT INTO users (email, name, role, company_id) VALUES 
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s)
                """, (
                    'admin@techcorp.com', 'TechCorp Admin', 'admin', techcorp_id,
                    'john@techcorp.com', 'John Doe', 'user', techcorp_id,
                    'jane@techcorp.com', 'Jane Smith', 'user', techcorp_id
                ))
                
                # Sample users for Innovate Solutions
                cursor.execute("""
                    INSERT INTO users (email, name, role, company_id) VALUES 
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s)
                """, (
                    'admin@innovate.com', 'Innovate Admin', 'admin', innovate_id,
                    'bob@innovate.com', 'Bob Johnson', 'user', innovate_id,
                    'alice@innovate.com', 'Alice Brown', 'user', innovate_id
                ))
            
            connection.commit()
            
            print("✅ Database setup completed successfully!")
            print("\n📊 Database Summary:")
            print("- 1 Superadmin: superadmin@system.com")
            print("- 3 Companies: System Admin, TechCorp Inc, Innovate Solutions")
            print("- 7 Users: 3 admins, 4 regular users")
            
            # Show tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n📋 Created tables: {', '.join([table[0] for table in tables])}")
            
            cursor.close()
            connection.close()
            
        else:
            print("❌ Failed to connect to MySQL server")
            
    except Error as e:
        print(f"❌ Database setup error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    setup_database() 