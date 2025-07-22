#!/usr/bin/env python3
"""
Superadmin Management Tool
Add superadmins to the database and send OTP via email
"""

import argparse
import sys
import os
from dotenv import load_dotenv
from database import get_superadmin_by_email, create_superadmin
from auth import generate_otp, get_otp_expiry, send_otp_email
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD

load_dotenv()

def add_superadmin(email: str, name: str):
    """Add a new superadmin to the database"""
    print(f"👑 Adding superadmin: {name} ({email})")
    print("=" * 50)
    
    # Check if superadmin already exists
    existing = get_superadmin_by_email(email)
    if existing:
        print(f"❌ Superadmin with email {email} already exists!")
        return False
    
    # Create superadmin in database
    superadmin_id = create_superadmin(email, name)
    if not superadmin_id:
        print("❌ Failed to create superadmin in database!")
        return False
    
    print(f"✅ Superadmin created with ID: {superadmin_id}")
    
    # Generate OTP
    otp = generate_otp()
    expiry = get_otp_expiry()
    
    print(f"📧 Sending OTP email to: {email}")
    print(f"🔢 OTP: {otp}")
    print(f"⏰ Expires: {expiry}")
    
    # Send OTP via email
    success = send_otp_email(email, otp, "Voice Assistant SaaS")
    
    if success:
        print("✅ OTP email sent successfully!")
        print("\n📋 Login Instructions:")
        print(f"1. Go to: http://localhost:5174")
        print(f"2. Click 'Superadmin Login'")
        print(f"3. Enter email: {email}")
        print(f"4. Click 'Send OTP'")
        print(f"5. Check your email for OTP: {otp}")
        print(f"6. Enter OTP and login")
    else:
        print("❌ Failed to send OTP email!")
        print("💡 Check your email configuration in .env file")
    
    return True

def list_superadmins():
    """List all superadmins in the database"""
    print("👑 Listing all superadmins...")
    print("=" * 50)
    
    try:
        from database import get_connection
        connection = get_connection()
        if not connection:
            print("❌ Failed to connect to database!")
            return
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, email, name, is_active, created_at FROM superadmins ORDER BY created_at DESC"
        cursor.execute(query)
        superadmins = cursor.fetchall()
        
        if not superadmins:
            print("📭 No superadmins found in database")
        else:
            print(f"📊 Found {len(superadmins)} superadmin(s):")
            print()
            for admin in superadmins:
                status = "✅ Active" if admin['is_active'] else "❌ Inactive"
                print(f"ID: {admin['id']}")
                print(f"Name: {admin['name']}")
                print(f"Email: {admin['email']}")
                print(f"Status: {status}")
                print(f"Created: {admin['created_at']}")
                print("-" * 30)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error listing superadmins: {e}")

def check_email_config():
    """Check if email configuration is properly set up"""
    print("📧 Checking email configuration...")
    print("=" * 50)
    
    required_vars = ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USER', 'EMAIL_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Hide password
            display_value = value if var != 'EMAIL_PASSWORD' else '*' * len(value)
            print(f"✅ {var}: {display_value}")
    
    if missing_vars:
        print(f"❌ Missing email configuration: {', '.join(missing_vars)}")
        print("\n💡 Add these to your .env file:")
        print("EMAIL_HOST=smtp.gmail.com")
        print("EMAIL_PORT=587")
        print("EMAIL_USER=your-email@gmail.com")
        print("EMAIL_PASSWORD=your-app-password")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Voice Assistant SaaS - Superadmin Management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add superadmin command
    add_parser = subparsers.add_parser('add', help='Add a new superadmin')
    add_parser.add_argument('email', help='Superadmin email address')
    add_parser.add_argument('name', help='Superadmin full name')
    
    # List superadmins command
    list_parser = subparsers.add_parser('list', help='List all superadmins')
    
    # Check email config command
    config_parser = subparsers.add_parser('check-email', help='Check email configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'add':
        if not check_email_config():
            print("\n❌ Please configure email settings before adding superadmins")
            return
        
        success = add_superadmin(args.email, args.name)
        if success:
            print("\n🎉 Superadmin added successfully!")
        else:
            print("\n❌ Failed to add superadmin!")
            sys.exit(1)
    
    elif args.command == 'list':
        list_superadmins()
    
    elif args.command == 'check-email':
        check_email_config()

if __name__ == "__main__":
    main() 