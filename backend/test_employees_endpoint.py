#!/usr/bin/env python3
"""Test the employees endpoint"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_employees_endpoint():
    """Test the employees endpoint"""
    print("Testing employees endpoint...")
    
    # Test public employees endpoint (should require authentication)
    try:
        response = requests.get(f"{BASE_URL}/employees")
        print(f"Public employees endpoint status: {response.status_code}")
        if response.status_code == 200:
            employees = response.json()
            print(f"Found {len(employees)} employees")
            for emp in employees[:3]:  # Show first 3
                print(f"  - {emp['name']} ({emp['department']})")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing public employees endpoint: {e}")
    
    # Test admin employees endpoint (should require admin auth)
    try:
        response = requests.get(f"{BASE_URL}/admin/employees")
        print(f"Admin employees endpoint status: {response.status_code}")
        if response.status_code == 200:
            employees = response.json()
            print(f"Found {len(employees)} employees")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing admin employees endpoint: {e}")

if __name__ == "__main__":
    test_employees_endpoint() 