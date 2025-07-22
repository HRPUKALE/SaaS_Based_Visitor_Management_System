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
    'password': os.getenv('DB_PASSWORD', ''),
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
            
            # Note: No default superadmin - use superadmin_manager.py to add them
            print("📝 Note: No default superadmin created")
            print("   Use: python superadmin_manager.py add <email> <name>")
            
            # Note: No sample data - will be created when superadmin is added
            print("📝 Note: No sample data created")
            print("   Companies and users will be created through the web interface")
            
            connection.commit()
            
            print("✅ Database setup completed successfully!")
            print("\n📊 Database Summary:")
            print("- 0 Superadmins (add via command line)")
            print("- 0 Companies (create via web interface)")
            print("- 0 Users (create via web interface)")
            
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