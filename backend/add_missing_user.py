#!/usr/bin/env python3
"""
Add the missing user to the database for voice assistant testing
"""

def add_missing_user():
    """Add the missing user to the database"""
    
    print("🔧 Adding Missing User to Database...")
    
    try:
        from database import get_connection, create_user
        
        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Check if user already exists
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, ("arhumzeenath20103@gmail.com",))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print("✅ User already exists!")
                print(f"ID: {existing_user['id']}")
                print(f"Email: {existing_user['email']}")
                print(f"Name: {existing_user['name']}")
                print(f"Role: {existing_user['role']}")
                print(f"Company ID: {existing_user['company_id']}")
                return
            
            # Check available companies
            query = "SELECT * FROM companies ORDER BY id"
            cursor.execute(query)
            companies = cursor.fetchall()
            
            print("📋 Available companies:")
            for company in companies:
                print(f"  ID: {company['id']} - {company['name']}")
            
            # Add user to company_id 1 (TechCorp Inc) as a user
            user_id = create_user(
                email="arhumzeenath20103@gmail.com",
                name="Arhum Khan",
                role="user",
                company_id=1  # TechCorp Inc
            )
            
            if user_id:
                print(f"✅ User created successfully! ID: {user_id}")
                print("📋 User details:")
                print(f"  Email: arhumzeenath20103@gmail.com")
                print(f"  Name: Arhum Khan")
                print(f"  Role: user")
                print(f"  Company ID: 1 (TechCorp Inc)")
                print("\n💡 Now the user can:")
                print("  1. Log out from frontend")
                print("  2. Log back in with arhumzeenath20103@gmail.com")
                print("  3. Test voice assistant booking")
            else:
                print("❌ Failed to create user")
            
            cursor.close()
            connection.close()
            
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Failed to add user: {e}")
        import traceback
        traceback.print_exc()

def verify_user_creation():
    """Verify the user was created successfully"""
    
    print(f"\n🔍 Verifying User Creation...")
    
    try:
        from database import get_connection
        
        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Check for the user
            query = """
                SELECT u.*, c.name as company_name 
                FROM users u 
                JOIN companies c ON u.company_id = c.id 
                WHERE u.email = %s
            """
            cursor.execute(query, ("arhumzeenath20103@gmail.com",))
            user = cursor.fetchone()
            
            if user:
                print("✅ User found in database!")
                print(f"ID: {user['id']}")
                print(f"Email: {user['email']}")
                print(f"Name: {user['name']}")
                print(f"Role: {user['role']}")
                print(f"Company ID: {user['company_id']}")
                print(f"Company Name: {user['company_name']}")
                print(f"Active: {user['is_active']}")
            else:
                print("❌ User not found in database")
            
            cursor.close()
            connection.close()
            
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    add_missing_user()
    verify_user_creation()
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("1. ✅ User should now be in database")
    print("2. 🔄 User needs to log out from frontend")
    print("3. 🔄 User needs to log back in with arhumzeenath20103@gmail.com")
    print("4. 🧪 Test voice assistant booking again")
    print("\n💡 The voice assistant should now work correctly!") 