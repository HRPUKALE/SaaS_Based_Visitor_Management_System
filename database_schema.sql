-- Voice Assistant SaaS Database Schema
-- Drop existing database if it exists
DROP DATABASE IF EXISTS voice_assistant_saas;

-- Create database
CREATE DATABASE voice_assistant_saas;
USE voice_assistant_saas;

-- 1. SUPERADMINS TABLE (System administrators)
CREATE TABLE superadmins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_active (is_active)
);

-- 2. COMPANIES TABLE (Organizations managed by superadmins)
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
);

-- 3. USERS TABLE (Company employees - both admins and regular users)
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
);

-- 4. EMPLOYEES TABLE (Store company employees)
CREATE TABLE employees (
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
);

-- 5. APPOINTMENTS TABLE (Store all appointment bookings)
CREATE TABLE appointments (
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

-- Insert default superadmin
INSERT INTO superadmins (email, name) VALUES 
('superadmin@system.com', 'System Administrator');

-- Insert default company for system admin
INSERT INTO companies (name, email, domain, created_by) VALUES 
('System Admin Company', 'admin@system.com', 'system.com', 1);

-- Insert default admin user for the system company
INSERT INTO users (email, name, role, company_id) VALUES 
('admin@system.com', 'System Admin', 'admin', 1);

-- Create additional indexes for better performance
CREATE INDEX idx_users_email_company ON users(email, company_id);
CREATE INDEX idx_companies_created_by_active ON companies(created_by, is_active);
CREATE INDEX idx_superadmins_email_active ON superadmins(email, is_active);

-- Add some sample data for testing
INSERT INTO companies (name, email, domain, created_by) VALUES 
('TechCorp Inc', 'contact@techcorp.com', 'techcorp.com', 1),
('Innovate Solutions', 'info@innovate.com', 'innovate.com', 1);

-- Add sample users for TechCorp
INSERT INTO users (email, name, role, company_id) VALUES 
('admin@techcorp.com', 'TechCorp Admin', 'admin', 2),
('john@techcorp.com', 'John Doe', 'user', 2),
('jane@techcorp.com', 'Jane Smith', 'user', 2);

-- Add sample users for Innovate Solutions
INSERT INTO users (email, name, role, company_id) VALUES 
('admin@innovate.com', 'Innovate Admin', 'admin', 3),
('bob@innovate.com', 'Bob Johnson', 'user', 3),
('alice@innovate.com', 'Alice Brown', 'user', 3);

-- Show the created tables
SHOW TABLES;

-- Show table structures
DESCRIBE superadmins;
DESCRIBE companies;
DESCRIBE users;
DESCRIBE appointments;

-- Show sample data
SELECT 'SUPERADMINS' as table_name;
SELECT * FROM superadmins;

SELECT 'COMPANIES' as table_name;
SELECT * FROM companies;

SELECT 'USERS' as table_name;
SELECT * FROM users; 