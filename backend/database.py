import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

# Superadmin functions
def get_superadmin_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get superadmin by email"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM superadmins WHERE email = %s AND is_active = TRUE"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error getting superadmin: {e}")
        return None

def create_superadmin(email: str, name: str) -> Optional[int]:
    """Create a new superadmin"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = "INSERT INTO superadmins (email, name) VALUES (%s, %s)"
        cursor.execute(query, (email, name))
        superadmin_id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        return superadmin_id
    except Error as e:
        logger.error(f"Error creating superadmin: {e}")
        return None

# Company functions
def create_company(name: str, email: str, domain: str, created_by: int) -> Optional[int]:
    """Create a new company"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = "INSERT INTO companies (name, email, domain, created_by) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, domain, created_by))
        company_id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        return company_id
    except Error as e:
        logger.error(f"Error creating company: {e}")
        return None

def get_company_by_id(company_id: int) -> Optional[Dict[str, Any]]:
    """Get company by ID"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM companies WHERE id = %s AND is_active = TRUE"
        cursor.execute(query, (company_id,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error getting company: {e}")
        return None

def get_company_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get company by email"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM companies WHERE email = %s AND is_active = TRUE"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error getting company by email: {e}")
        return None

def get_all_companies() -> List[Dict[str, Any]]:
    """Get all active companies"""
    try:
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT c.*, COALESCE(s.name, 'Unknown') as created_by_name 
            FROM companies c 
            LEFT JOIN superadmins s ON c.created_by = s.id 
            WHERE c.is_active = TRUE 
            ORDER BY c.created_at DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return results
    except Error as e:
        logger.error(f"Error getting all companies: {e}")
        return []

def get_companies_by_superadmin(superadmin_id: int) -> List[Dict[str, Any]]:
    """Get companies created by a specific superadmin"""
    try:
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM companies WHERE created_by = %s AND is_active = TRUE ORDER BY created_at DESC"
        cursor.execute(query, (superadmin_id,))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return results
    except Error as e:
        logger.error(f"Error getting companies by superadmin: {e}")
        return []

# User functions
def create_user(email: str, name: str, role: str, company_id: int) -> Optional[int]:
    """Create a new user"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = "INSERT INTO users (email, name, role, company_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email, name, role, company_id))
        user_id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        return user_id
    except Error as e:
        logger.error(f"Error creating user: {e}")
        return None

def get_user_by_email_and_company(email: str, company_id: int) -> Optional[Dict[str, Any]]:
    """Get user by email and company"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.*, c.name as company_name 
            FROM users u 
            JOIN companies c ON u.company_id = c.id 
            WHERE u.email = %s AND u.company_id = %s AND u.is_active = TRUE
        """
        cursor.execute(query, (email, company_id))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error getting user: {e}")
        return None

def get_users_by_company(company_id: int) -> List[Dict[str, Any]]:
    """Get all users in a company"""
    try:
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.*, c.name as company_name 
            FROM users u 
            JOIN companies c ON u.company_id = c.id 
            WHERE u.company_id = %s AND u.is_active = TRUE 
            ORDER BY u.created_at DESC
        """
        cursor.execute(query, (company_id,))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return results
    except Error as e:
        logger.error(f"Error getting users by company: {e}")
        return []

def update_user_otp(user_id: int, otp: str, expiry: str) -> bool:
    """Update user OTP"""
    try:
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "UPDATE users SET otp = %s, otp_expiry = %s WHERE id = %s"
        cursor.execute(query, (otp, expiry, user_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        logger.error(f"Error updating user OTP: {e}")
        return False

def verify_user_otp(email: str, company_id: int, otp: str) -> Optional[Dict[str, Any]]:
    """Verify user OTP"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM users 
            WHERE email = %s AND company_id = %s AND otp = %s 
            AND otp_expiry > NOW() AND is_active = TRUE
        """
        cursor.execute(query, (email, company_id, otp))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error verifying user OTP: {e}")
        return None

def clear_user_otp(user_id: int) -> bool:
    """Clear user OTP after successful verification"""
    try:
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "UPDATE users SET otp = NULL, otp_expiry = NULL, last_login = NOW() WHERE id = %s"
        cursor.execute(query, (user_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        logger.error(f"Error clearing user OTP: {e}")
        return False

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.*, c.name as company_name 
            FROM users u 
            JOIN companies c ON u.company_id = c.id 
            WHERE u.id = %s AND u.is_active = TRUE
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error getting user by ID: {e}")
        return None 

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email (first match, any company)"""
    try:
        connection = get_connection()
        if not connection:
            return None
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.*, c.name as company_name 
            FROM users u 
            JOIN companies c ON u.company_id = c.id 
            WHERE u.email = %s AND u.is_active = TRUE 
            LIMIT 1
        """
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None

def get_user_by_email_and_role(email: str, role: str) -> Optional[Dict[str, Any]]:
    """Get user by email and role (first match, any company)"""
    try:
        connection = get_connection()
        if not connection:
            return None
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.*, c.name as company_name 
            FROM users u 
            JOIN companies c ON u.company_id = c.id 
            WHERE u.email = %s AND u.role = %s AND u.is_active = TRUE 
            LIMIT 1
        """
        cursor.execute(query, (email, role))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        logger.error(f"Error getting user by email and role: {e}")
        return None 

# Appointment functions
def create_appointment(
    employee_name: str,
    department: str,
    reason: str,
    appointment_date: str,
    appointment_time: str,
    visitor_name: str,
    visitor_email: str,
    visitor_phone: str,
    company_id: int,
    booking_method: str = 'manual'
) -> Optional[int]:
    """Create a new appointment"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = """
            INSERT INTO appointments 
            (employee_name, department, reason, appointment_date, appointment_time, 
             visitor_name, visitor_email, visitor_phone, company_id, booking_method) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            employee_name, department, reason, appointment_date, appointment_time,
            visitor_name, visitor_email, visitor_phone, company_id, booking_method
        ))
        appointment_id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        return appointment_id
    except Error as e:
        logger.error(f"Error creating appointment: {e}")
        return None

def get_appointment_by_id(appointment_id: int) -> Optional[Dict[str, Any]]:
    """Get appointment by ID"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT a.*, c.name as company_name 
            FROM appointments a 
            JOIN companies c ON a.company_id = c.id 
            WHERE a.id = %s
        """
        cursor.execute(query, (appointment_id,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error getting appointment by ID: {e}")
        return None

def get_appointments_by_company(company_id: int) -> List[Dict[str, Any]]:
    """Get all appointments for a company"""
    try:
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT a.*, c.name as company_name 
            FROM appointments a 
            JOIN companies c ON a.company_id = c.id 
            WHERE a.company_id = %s 
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        cursor.execute(query, (company_id,))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return results
    except Error as e:
        logger.error(f"Error getting appointments by company: {e}")
        return []

def get_appointments_by_visitor_email(visitor_email: str) -> List[Dict[str, Any]]:
    """Get all appointments for a visitor by email"""
    try:
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT a.*, c.name as company_name 
            FROM appointments a 
            JOIN companies c ON a.company_id = c.id 
            WHERE a.visitor_email = %s 
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        cursor.execute(query, (visitor_email,))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return results
    except Error as e:
        logger.error(f"Error getting appointments by visitor email: {e}")
        return []

def update_appointment_status(appointment_id: int, status: str) -> bool:
    """Update appointment status"""
    try:
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "UPDATE appointments SET status = %s WHERE id = %s"
        cursor.execute(query, (status, appointment_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        logger.error(f"Error updating appointment status: {e}")
        return False

def mark_appointment_email_sent(appointment_id: int) -> bool:
    """Mark appointment email as sent"""
    try:
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "UPDATE appointments SET email_sent = TRUE WHERE id = %s"
        cursor.execute(query, (appointment_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        logger.error(f"Error marking appointment email sent: {e}")
        return False

def mark_appointment_qr_sent(appointment_id: int) -> bool:
    """Mark appointment QR code as sent"""
    try:
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "UPDATE appointments SET qr_code_sent = TRUE WHERE id = %s"
        cursor.execute(query, (appointment_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        logger.error(f"Error marking appointment QR sent: {e}")
        return False

# Employee functions
def create_employee(name: str, email: str, department: str, designation: str, phone: str, company_id: int) -> Optional[int]:
    """Create a new employee"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = """
            INSERT INTO employees (name, email, department, designation, phone, company_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, department, designation, phone, company_id))
        employee_id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        return employee_id
    except Error as e:
        logger.error(f"Error creating employee: {e}")
        return None

def get_employees_by_company(company_id: int) -> List[Dict[str, Any]]:
    """Get all employees for a company"""
    try:
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM employees 
            WHERE company_id = %s AND is_active = TRUE 
            ORDER BY name ASC
        """
        cursor.execute(query, (company_id,))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return results
    except Error as e:
        logger.error(f"Error getting employees by company: {e}")
        return []

def get_employee_by_email_and_company(email: str, company_id: int) -> Optional[Dict[str, Any]]:
    """Get employee by email and company"""
    try:
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM employees 
            WHERE email = %s AND company_id = %s AND is_active = TRUE
        """
        cursor.execute(query, (email, company_id))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        logger.error(f"Error getting employee by email and company: {e}")
        return None

def get_employees_by_department(company_id: int, department: str) -> List[Dict[str, Any]]:
    """Get employees by department"""
    try:
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM employees 
            WHERE company_id = %s AND department = %s AND is_active = TRUE 
            ORDER BY name ASC
        """
        cursor.execute(query, (company_id, department))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return results
    except Error as e:
        logger.error(f"Error getting employees by department: {e}")
        return []

def update_employee(employee_id: int, name: str, email: str, department: str, designation: str, phone: str) -> bool:
    """Update employee details"""
    try:
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = """
            UPDATE employees 
            SET name = %s, email = %s, department = %s, designation = %s, phone = %s 
            WHERE id = %s
        """
        cursor.execute(query, (name, email, department, designation, phone, employee_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        logger.error(f"Error updating employee: {e}")
        return False

def deactivate_employee(employee_id: int) -> bool:
    """Deactivate employee"""
    try:
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "UPDATE employees SET is_active = FALSE WHERE id = %s"
        cursor.execute(query, (employee_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        logger.error(f"Error deactivating employee: {e}")
        return False 