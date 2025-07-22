#!/usr/bin/env python3
"""
Test script to verify JWT token creation and verification
"""

from auth import create_access_token, verify_token
from database import get_superadmin_by_email
import jwt

def test_token_creation():
    print("🔍 Testing JWT Token Creation and Verification...")
    print("=" * 60)
    
    # Test data
    test_data = {
        "superadmin_id": 1,
        "email": "harshadpukale131@gmail.com",
        "role": "superadmin",
        "name": "HRP"
    }
    
    print(f"Creating token with data: {test_data}")
    
    # Create token
    token = create_access_token(test_data)
    print(f"Generated token: {token}")
    print(f"Token length: {len(token)}")
    
    # Verify token
    payload = verify_token(token)
    print(f"Verified payload: {payload}")
    print(f"Payload keys: {list(payload.keys())}")
    print(f"Superadmin ID in payload: {payload.get('superadmin_id')}")
    
    # Test with actual superadmin from database
    print("\n" + "=" * 60)
    print("Testing with actual superadmin from database...")
    
    superadmin = get_superadmin_by_email("harshadpukale131@gmail.com")
    if superadmin:
        print(f"Found superadmin: {superadmin}")
        
        # Create token with real data
        real_token_data = {
            "superadmin_id": superadmin["id"],
            "email": superadmin["email"],
            "role": "superadmin",
            "name": superadmin["name"]
        }
        
        print(f"Creating token with real data: {real_token_data}")
        real_token = create_access_token(real_token_data)
        print(f"Real token: {real_token[:50]}...")
        
        # Verify real token
        real_payload = verify_token(real_token)
        print(f"Real payload: {real_payload}")
        print(f"Real payload keys: {list(real_payload.keys())}")
        print(f"Real superadmin ID: {real_payload.get('superadmin_id')}")
        
    else:
        print("❌ Superadmin not found in database!")
        print("💡 Make sure you've added the superadmin using:")
        print("   python superadmin_manager.py add harshadpukale131@gmail.com \"HRP\"")
    
    print("=" * 60)

if __name__ == "__main__":
    test_token_creation() 