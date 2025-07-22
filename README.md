# Voice Assistant SaaS Platform

A multi-tenant SaaS platform for AI Voice Assistant with role-based access control.

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Authentication**: JWT + OTP (Email-based)

## 👥 User Roles

1. **Superadmin**: Can create companies
2. **Admin**: Can create users for their company
3. **User**: Can access voice assistant

## 🚀 Quick Start

### 1. Database Setup

Run the following MySQL commands in your MySQL Workbench:

```sql
-- Create database for SaaS Voice Assistant
CREATE DATABASE IF NOT EXISTS voice_assistant_saas;
USE voice_assistant_saas;

-- Companies table
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    company_id INT NOT NULL,
    otp VARCHAR(6) NULL,
    otp_expiry TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    UNIQUE KEY unique_email_per_company (email, company_id)
);

-- Insert default superadmin company
INSERT INTO companies (name, email) VALUES ('System Admin', 'superadmin@system.com');

-- Create indexes
CREATE INDEX idx_users_company_id ON users(company_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_otp ON users(otp);
CREATE INDEX idx_companies_email ON companies(email);
```

### 2. Backend Setup

```bash
cd backend

# Option 1: Use the setup script (recommended)
python setup.py

# Option 2: Manual installation
# For Python 3.13+ (minimal dependencies to avoid NumPy issues)
pip install -r requirements_minimal.txt

# For Python 3.12 and below
pip install -r requirements.txt

# If you encounter NumPy compilation issues, try:
pip install fastapi uvicorn pymysql python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv email-validator requests

# The setup script will create .env file automatically
# Edit .env with your database and email settings:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=voice_assistant_saas
# JWT_SECRET_KEY=your-secret-key
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USER=your-email@gmail.com
# EMAIL_PASSWORD=your-app-password

# Check available ports (optional)
python check_port.py

# Start the server
python start_server.py

# If you get port errors, try:
# set PORT=8002 && python start_server.py
# or
# python check_port.py
```

### 3. Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔐 Authentication Flow

### Superadmin Login
1. Go to `/superadmin`
2. Enter email: `superadmin@system.com`
3. Enter any 6-digit OTP (for demo purposes)
4. Access company management dashboard

### Admin Login
1. Go to `/admin`
2. Select company
3. Enter admin email
4. Verify OTP sent to email
5. Access user management dashboard

### User Login
1. Go to `/user`
2. Select company
3. Enter user email
4. Verify OTP sent to email
5. Access voice assistant

## 📁 Project Structure

```
project/
├── backend/
│   ├── saas_api.py          # Main FastAPI application
│   ├── database.py          # Database utilities
│   ├── auth.py              # Authentication utilities
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration
│   ├── requirements.txt     # Python dependencies
│   └── start_server.py      # Server startup script
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SuperadminLogin.tsx
│   │   │   ├── SuperadminDashboard.tsx
│   │   │   ├── AdminLogin.tsx
│   │   │   ├── AdminDashboard.tsx
│   │   │   ├── UserLogin.tsx
│   │   │   └── VoiceAssistant.tsx
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── App.tsx
│   └── package.json
└── database_schema.sql
```

## 🔧 API Endpoints

### Superadmin
- `POST /superadmin/login` - Send OTP
- `POST /superadmin/verify-otp` - Verify OTP
- `POST /superadmin/companies` - Create company
- `GET /superadmin/companies` - List companies

### Admin
- `POST /admin/login` - Send OTP
- `POST /admin/verify-otp` - Verify OTP
- `POST /admin/users` - Create user
- `GET /admin/users` - List users

### User
- `POST /user/login` - Send OTP
- `POST /user/verify-otp` - Verify OTP
- `GET /user/profile` - Get profile

## 🎯 Features

- ✅ Multi-tenant architecture
- ✅ Role-based access control
- ✅ Email-based OTP authentication
- ✅ JWT token management
- ✅ Company and user management
- ✅ Voice assistant integration
- ✅ Responsive UI with Tailwind CSS
- ✅ TypeScript for type safety

## 🔒 Security Features

- JWT token authentication
- OTP expiration (5 minutes)
- Role-based route protection
- Email validation
- Unique constraints on database

## 🚨 Important Notes

1. **Email Configuration**: For production, configure proper SMTP settings in `.env`
2. **JWT Secret**: Change the JWT secret key in production
3. **Database**: Use strong passwords for database access
4. **HTTPS**: Enable HTTPS in production
5. **OTP**: Currently using mock email sending for development

## 🐛 Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check database credentials in `.env`
- Ensure database exists

### Email Issues
- Check SMTP settings in `.env`
- For Gmail, use App Password instead of regular password
- Verify email credentials

### Frontend Issues
- Clear browser cache
- Check console for errors
- Verify API endpoint URLs

### Port Issues
- Run `python check_port.py` to find available ports
- Try different ports: `set PORT=8002 && python start_server.py`
- Close other applications using the same port
- Run as administrator if needed
- Update frontend API URL if using different port

## 📝 License

This project is for educational purposes. Modify as needed for production use. 