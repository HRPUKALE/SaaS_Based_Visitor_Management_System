Here's the updated `README.md` with a new **🧠 Workflow** and **🎯 Use Cases** section added. These sections explain the real-world workflow and purpose of the project:


### Voice Assistant SaaS Platform

A **multi-tenant SaaS platform** for an AI Voice Assistant with **role-based access control**, email-based OTP authentication, and voice-enabled appointment or service interaction.


## 🏗️ Architecture

- **Frontend:** React + TypeScript + Tailwind CSS  
- **Backend:** FastAPI (Python)  
- **Database:** MySQL  
- **Authentication:** JWT + OTP (Email-based)  

---

## 👥 User Roles

- **Superadmin**: Can create and manage companies
- **Admin**: Can create users for their assigned company
- **User**: Can access the voice assistant service interface

---

## 🧠 Workflow

1. **Superadmin Onboards Company**
   - Logs in using a static email (e.g., `superadmin@system.com`)
   - Creates a new company and assigns an official email (used by company Admin)

2. **Admin Logs In**
   - Admin enters their email and receives a one-time password (OTP)
   - On verification, gets access to the admin dashboard
   - Creates multiple users (staff members) for the company

3. **User Logs In**
   - User selects company and enters email
   - Receives OTP for login, then gets access to the voice assistant dashboard

4. **Voice Assistant Interaction**
   - User can either manually book appointments or interact with the AI voice assistant
   - The voice assistant helps users schedule tasks, collect data, or manage bookings based on custom flows

5. **Database Records**
   - All users, roles, companies, and interactions are stored securely in the MySQL database

---

## 🎯 Use Cases

- **Visitor Management Systems (VMS)** with multilingual voice support
- **Appointment Booking Platforms** for clinics, banks, or service centers
- **Smart Receptionist** for physical kiosks at company entrances
- **Customer Support Interface** via voice
- **Voice-enabled Cafeteria or Amenity Services**
- Can be embedded into mobile/web apps for any domain needing voice automation

---

## 🚀 Quick Start

### 1. Database Setup

Run these SQL commands in your MySQL Workbench:

```sql
-- Create and use database
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

-- Insert default Superadmin
INSERT INTO companies (name, email) VALUES ('System Admin', 'superadmin@system.com');

-- Indexes
CREATE INDEX idx_users_company_id ON users(company_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_otp ON users(otp);
CREATE INDEX idx_companies_email ON companies(email);
````

---

### 2. Backend Setup

```bash
cd backend

# Option 1: Recommended (setup script)
python setup.py

# Option 2: Manual setup
pip install -r requirements.txt
```

Edit `.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=voice_assistant_saas
JWT_SECRET_KEY=your-secret-key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

Start server:

```bash
python start_server.py
```

---

### 3. Frontend Setup

```bash
cd Frontend
npm install
npm run dev
```

---

## 🔐 Authentication Flow

### Superadmin

* URL: `/superadmin`
* Email: `superadmin@system.com`
* Enter any 6-digit OTP (for demo)

### Admin

* URL: `/admin`
* Select company, enter email, receive OTP
* Manage company users

### User

* URL: `/user`
* Select company, enter email, receive OTP
* Access voice assistant screen

---

## 📁 Project Structure

```
project/
├── backend/
│   ├── saas_api.py
│   ├── database.py
│   ├── auth.py
│   ├── models.py
│   ├── config.py
│   ├── requirements.txt
│   └── start_server.py
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

---

## 🔧 API Endpoints

### Superadmin

* `POST /superadmin/login`
* `POST /superadmin/verify-otp`
* `POST /superadmin/companies`
* `GET /superadmin/companies`

### Admin

* `POST /admin/login`
* `POST /admin/verify-otp`
* `POST /admin/users`
* `GET /admin/users`

### User

* `POST /user/login`
* `POST /user/verify-otp`
* `GET /user/profile`

---

## ✅ Features

* Multi-tenant SaaS architecture
* Role-based route protection
* Email-based OTP (valid 5 minutes)
* JWT-based token security
* Voice assistant integration with UI
* React + TypeScript + Tailwind frontend
* FastAPI + MySQL backend
* Superadmin/Admin/User role dashboards

---

## 🔒 Security

* JWT token authentication
* OTP expiration
* Email validation and uniqueness
* Database-level constraints
* Environment-based secret management

---

## 🐛 Troubleshooting

**Database Errors**

* Ensure MySQL is running
* Validate `.env` credentials

**Email OTP Issues**

* Use correct SMTP (e.g., Gmail App Password)
* Enable less secure app access (if testing)

**Port Issues**

* Run `python check_port.py`
* Or use a different port: `set PORT=8002 && python start_server.py`

**Frontend Issues**

* Clear browser cache
* Verify console/API errors

---

## 📝 License

This project is open for educational and personal use. Modify as needed for production deployment.


