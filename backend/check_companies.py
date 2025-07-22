#!/usr/bin/env python3
"""Check companies and users in the database"""

from database import get_all_companies, get_users_by_company

def main():
    print("=== Companies ===")
    companies = get_all_companies()
    for company in companies:
        print(f"ID: {company['id']}, Name: {company['name']}, Email: {company['email']}")
        
        # Get users for this company
        users = get_users_by_company(company['id'])
        print(f"  Users:")
        for user in users:
            print(f"    - {user['email']} (role: {user['role']}, company_name: {user.get('company_name', 'N/A')})")
        print()

if __name__ == "__main__":
    main() 