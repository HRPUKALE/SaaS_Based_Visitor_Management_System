#!/usr/bin/env python3
"""
Debug script to test JWT authentication
"""

from auth import create_access_token, verify_token
import jwt
from datetime import datetime

def test_jwt():
    print("Testing JWT Authentication...")
    print("=" * 50)
    
    # Test data
    test_data = {
        "email": "superadmin@system.com",
        "role": "superadmin",
        "company_id": 1
    }
    
    print(f"Creating token with data: {test_data}")
    
    # Create token
    token = create_access_token(test_data)
    print(f"Generated token: {token}")
    print(f"Token length: {len(token)}")
    
    # Verify token
    payload = verify_token(token)
    print(f"Verified payload: {payload}")
    
    # Test with invalid token
    invalid_token = "invalid.token.here"
    invalid_payload = verify_token(invalid_token)
    print(f"Invalid token result: {invalid_payload}")
    
    print("=" * 50)
    print("JWT Test completed!")

if __name__ == "__main__":
    test_jwt() 