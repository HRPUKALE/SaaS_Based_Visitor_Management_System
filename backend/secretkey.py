import secrets

# Generate a secure 256-bit (32-byte) JWT secret key in hex format
jwt_secret = secrets.token_hex(32)

print("Your JWT Secret Key:")
print(jwt_secret)
