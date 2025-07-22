#!/usr/bin/env python3
"""
Helper script to generate OTP for admin login
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_user_by_email, update_user_otp
from auth import generate_otp, get_otp_expiry

def generate_admin_otp(admin_email):
    """Generate OTP for admin login"""
    print(f"Generating OTP for admin: {admin_email}")
    
    # Check if admin exists
    admin_user = get_user_by_email(admin_email)
    if not admin_user:
        print(f"❌ Admin user {admin_email} not found!")
        return None
    
    if admin_user['role'] != 'admin':
        print(f"❌ User {admin_email} is not an admin (role: {admin_user['role']})")
        return None
    
    # Generate OTP
    otp = generate_otp()
    expiry = get_otp_expiry()
    update_user_otp(admin_user['id'], otp, expiry)
    
    print(f"✅ OTP generated successfully!")
    print(f"📧 Email: {admin_email}")
    print(f"🔢 OTP: {otp}")
    print(f"⏰ Expires: {expiry}")
    print(f"🏢 Company: {admin_user.get('company_name', 'Unknown')}")
    print(f"👤 Name: {admin_user['name']}")
    
    return otp

if __name__ == "__main__":
    admin_email = "harshadpukale131@gmail.com"
    generate_admin_otp(admin_email) 