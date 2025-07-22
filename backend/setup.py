#!/usr/bin/env python3
"""
Setup script for Voice Assistant SaaS Backend
Handles dependency installation and environment setup
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=voice_assistant_saas

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Email Configuration (for OTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created. Please edit it with your actual credentials.")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Setting up Voice Assistant SaaS Backend...")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor >= 13:
        print("⚠️  Python 3.13+ detected. Using minimal requirements to avoid compatibility issues.")
        requirements_file = "requirements_minimal.txt"
    else:
        requirements_file = "requirements.txt"
    
    # Install dependencies
    if not run_command(f"pip install -r {requirements_file}", f"Installing dependencies from {requirements_file}"):
        print("\n🔧 Alternative installation methods:")
        print("1. Try installing dependencies one by one:")
        print("   pip install fastapi uvicorn pymysql python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv email-validator requests")
        print("\n2. If you need Streamlit and OpenAI, install them separately:")
        print("   pip install streamlit openai")
        print("\n3. Use conda instead of pip:")
        print("   conda install fastapi uvicorn pymysql python-multipart python-jose passlib python-dotenv email-validator requests")
        return False
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your database and email credentials")
    print("2. Run the database setup SQL commands in MySQL Workbench")
    print("3. Start the server: python start_server.py")
    print("\n🔗 Useful URLs:")
    print("- API Documentation: http://localhost:8000/docs")
    print("- Health Check: http://localhost:8000/health")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 