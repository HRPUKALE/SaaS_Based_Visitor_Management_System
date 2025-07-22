from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import logging
from datetime import datetime

from models import *
from database import (
    get_superadmin_by_email, create_superadmin,
    create_company as db_create_company, get_company_by_id, get_company_by_email, get_all_companies, get_companies_by_superadmin,
    create_user as db_create_user, get_user_by_email_and_company, get_users_by_company, get_user_by_id, get_user_by_email, get_user_by_email_and_role,
    update_user_otp, verify_user_otp, clear_user_otp,
    create_appointment, get_appointment_by_id, get_appointments_by_company, get_appointments_by_visitor_email,
    update_appointment_status, mark_appointment_email_sent, mark_appointment_qr_sent,
    create_employee as db_create_employee, get_employees_by_company, get_employee_by_email_and_company
)
from auth import create_access_token, verify_token, generate_otp, get_otp_expiry, send_otp_email
from email_service import email_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Assistant SaaS API", version="1.0.0")

# CORS middleware - Allow all localhost origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Dependency to get current user from token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    logger.info(f"Received token: {token[:20]}...")  # Log first 20 chars of token
    
    payload = verify_token(token)
    logger.info(f"Token payload: {payload}")
    
    if payload is None:
        logger.error("Token verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log all keys in the payload
    logger.info(f"Token payload keys: {list(payload.keys())}")
    logger.info(f"Superadmin ID in payload: {payload.get('superadmin_id')}")
    
    return payload

# Superadmin endpoints
@app.post("/superadmin/login", response_model=dict)
async def superadmin_login(request: SuperadminLoginRequest):
    """Superadmin login - sends OTP"""
    try:
        logger.info(f"Superadmin login attempt for email: {request.email}")
        
        # Check if superadmin exists in database
        superadmin = get_superadmin_by_email(request.email)
        if not superadmin:
            raise HTTPException(status_code=404, detail="Superadmin not found")
        
        # Generate OTP
        logger.info("Generating OTP...")
        otp = generate_otp()
        expiry = get_otp_expiry()
        logger.info(f"OTP generated: {otp}")
        
        # Send OTP via email
        logger.info("Sending OTP email...")
        success = send_otp_email(request.email, otp, "Voice Assistant SaaS")
        logger.info(f"OTP email result: {success}")
        
        if success:
            return {"message": "OTP sent successfully", "email": request.email}
        else:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Superadmin login error: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/superadmin/verify-otp", response_model=dict)
async def superadmin_verify_otp(request: SuperadminOTPVerifyRequest):
    """Superadmin OTP verification"""
    try:
        # For demo purposes, accept any 6-digit OTP for superadmin
        if len(request.otp) == 6 and request.otp.isdigit():
            # Get superadmin from database
            superadmin = get_superadmin_by_email(request.email)
            if not superadmin:
                raise HTTPException(status_code=404, detail="Superadmin not found")
            
            # Create superadmin token with proper data
            token_data = {
                "superadmin_id": superadmin["id"],
                "email": superadmin["email"],
                "role": "superadmin",
                "name": superadmin["name"]
            }
            access_token = create_access_token(token_data)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": superadmin["id"],
                    "email": superadmin["email"],
                    "name": superadmin["name"],
                    "role": "superadmin",
                    "company_id": None  # Superadmins don't belong to a specific company
                }
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Superadmin OTP verification error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/superadmin/companies", response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new company (Superadmin only) and auto-create admin user"""
    try:
        logger.info(f"Create company request - current_user: {current_user}")
        # Check if user is superadmin
        if current_user.get("role") != "superadmin":
            logger.error(f"Access denied - user role: {current_user.get('role')}")
            raise HTTPException(status_code=403, detail="Access denied")
        # Get superadmin ID from token
        superadmin_id = current_user.get("superadmin_id")
        logger.info(f"Superadmin ID from token: {superadmin_id}")
        if not superadmin_id:
            logger.error("No superadmin_id in token")
            raise HTTPException(status_code=400, detail="Invalid superadmin token")
        # Check if company email already exists
        existing_company = get_company_by_email(company.email)
        if existing_company:
            raise HTTPException(status_code=400, detail="Company email already exists")
        # Create company
        company_id = db_create_company(
            company.name, 
            company.email, 
            company.domain or "", 
            superadmin_id
        )
        if not company_id:
            raise HTTPException(status_code=500, detail="Failed to create company")
        new_company = get_company_by_id(company_id)
        if not new_company:
            raise HTTPException(status_code=500, detail="Failed to retrieve created company")
        # Automatically create admin user for the company
        from database import get_user_by_email_and_company, create_user
        admin_email = company.email
        admin_name = company.name + " Admin"
        existing_admin = get_user_by_email_and_company(admin_email, company_id)
        if not existing_admin:
            create_user(admin_email, admin_name, "admin", company_id)
            logger.info(f"Auto-created admin user for company: {admin_email}")
        else:
            logger.info(f"Admin user already exists for company: {admin_email}")
        return CompanyResponse(**new_company)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create company error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/superadmin/companies", response_model=List[CompanyResponse])
async def get_companies(current_user: dict = Depends(get_current_user)):
    """Get all companies (Superadmin only)"""
    try:
        # Check if user is superadmin
        if current_user.get("role") != "superadmin":
            raise HTTPException(status_code=403, detail="Access denied")
        
        companies = get_all_companies()
        return [CompanyResponse(**company) for company in companies]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get companies error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/superadmin/companies/{company_id}/admin", response_model=UserResponse)
async def create_company_admin(company_id: int, user: UserCreate, current_user: dict = Depends(get_current_user)):
    """Superadmin creates an admin user for a company"""
    if current_user.get("role") != "superadmin":
        raise HTTPException(status_code=403, detail="Access denied")
    company = get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    # Check if admin already exists for this company
    existing_admin = get_user_by_email_and_company(user.email, company_id)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists in this company")
    # Create admin user
    user_id = db_create_user(user.email, user.name, "admin", company_id)
    new_user = get_user_by_email_and_company(user.email, company_id)
    return UserResponse(**new_user)

# Admin endpoints
@app.post("/admin/login", response_model=dict)
async def admin_login(request: AdminLoginRequest):
    """Admin login - sends OTP (email + role)"""
    try:
        logger.info(f"🔍 Admin login request for email: {request.email}, role: {request.role}")
        
        # Validate role
        if request.role not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'user'")
        
        # Look up user by email and role
        user = get_user_by_email_and_role(request.email, request.role)
        logger.info(f"📋 User found: {user}")
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found with email {request.email} and role {request.role}")
        if user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not an admin")
        if not user["is_active"]:
            raise HTTPException(status_code=403, detail="User account is deactivated")
        
        # Generate and store OTP
        otp = generate_otp()
        expiry = get_otp_expiry()
        update_user_otp(user["id"], otp, expiry)
        
        # Send OTP email
        company = get_company_by_id(user["company_id"])
        success = send_otp_email(request.email, otp, company["name"] if company else "Your Company")
        if success:
            logger.info(f"✅ OTP sent successfully for {request.email} with role {request.role}")
            return {"message": "OTP sent successfully", "email": request.email, "role": request.role}
        else:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/admin/verify-otp", response_model=TokenResponse)
async def admin_verify_otp(request: AdminOTPVerifyRequest):
    """Admin OTP verification (email + otp + role)"""
    try:
        logger.info(f"🔍 Admin verify OTP called for email: {request.email}, role: {request.role}")
        
        # Validate role
        if request.role not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'user'")
        
        # Look up user by email and role
        user = get_user_by_email_and_role(request.email, request.role)
        logger.info(f"📋 User found: {user}")
        
        if not user or user["role"] != "admin":
            raise HTTPException(status_code=404, detail=f"Admin user not found with email {request.email} and role {request.role}")
        
        # Verify OTP
        if not user["otp"] or user["otp"] != request.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        # Clear OTP after successful verification
        clear_user_otp(user["id"])
        
        # Create access token
        token_data = {
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "company_id": user["company_id"]
        }
        logger.info(f"🔐 Token data: {token_data}")
        access_token = create_access_token(token_data)
        
        response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(**user)
        )
        
        logger.info(f"✅ Admin verify OTP response: user role = {response.user.role}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin OTP verification error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/admin/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new user (Admin only)"""
    try:
        # Check if user is admin
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        company_id = current_user.get("company_id")
        if not user.name:
            raise HTTPException(status_code=400, detail="Name is required")
        # Check if user already exists in company
        existing_user = get_user_by_email_and_company(user.email, company_id)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists in company")
        # Create user
        user_id = db_create_user(user.email, user.name, user.role, company_id)
        new_user = get_user_by_email_and_company(user.email, company_id)
        return UserResponse(**new_user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create user error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/admin/users", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_user)):
    """Get all users for company (Admin only)"""
    try:
        # Check if user is admin
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        
        company_id = current_user.get("company_id")
        users = get_users_by_company(company_id)
        
        return [UserResponse(**user) for user in users]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get users error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Employee endpoints (Admin only)
@app.post("/admin/employees", response_model=EmployeeResponse)
async def create_employee(
    employee: EmployeeCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new employee (Admin only)"""
    try:
        # Check if user is admin
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        
        company_id = current_user.get("company_id")
        
        # Check if employee already exists in company
        existing_employee = get_employee_by_email_and_company(employee.email, company_id)
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee already exists in company")
        
        # Create employee
        employee_id = db_create_employee(
            employee.name,
            employee.email,
            employee.department,
            employee.designation or "",
            employee.phone or "",
            company_id
        )
        
        if not employee_id:
            raise HTTPException(status_code=500, detail="Failed to create employee")
        
        # Get the created employee
        new_employee = get_employee_by_email_and_company(employee.email, company_id)
        if not new_employee:
            raise HTTPException(status_code=500, detail="Failed to retrieve created employee")
        
        return EmployeeResponse(**new_employee)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create employee error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/admin/employees", response_model=List[EmployeeResponse])
async def get_employees(current_user: dict = Depends(get_current_user)):
    """Get all employees for company (Admin only)"""
    try:
        # Check if user is admin
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        
        company_id = current_user.get("company_id")
        employees = get_employees_by_company(company_id)
        
        return [EmployeeResponse(**employee) for employee in employees]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get employees error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/admin/employees/upload-csv")
async def upload_employees_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload employees via CSV (Admin only)"""
    try:
        # Check if user is admin
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        
        company_id = current_user.get("company_id")
        
        # Check file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read CSV content
        content = await file.read()
        csv_text = content.decode('utf-8')
        
        # Parse CSV
        import csv
        from io import StringIO
        
        csv_file = StringIO(csv_text)
        reader = csv.DictReader(csv_file)
        
        created_count = 0
        errors = []
        
        for row_num, row in enumerate(reader, start=2):  # Start from 2 to account for header
            try:
                # Validate required fields
                if not row.get('name') or not row.get('email') or not row.get('department'):
                    errors.append(f"Row {row_num}: Missing required fields (name, email, department)")
                    continue
                
                # Check if employee already exists
                existing_employee = get_employee_by_email_and_company(row['email'], company_id)
                if existing_employee:
                    errors.append(f"Row {row_num}: Employee with email {row['email']} already exists")
                    continue
                
                # Create employee
                employee_id = db_create_employee(
                    row['name'],
                    row['email'],
                    row['department'],
                    row.get('designation', ''),
                    row.get('phone', ''),
                    company_id
                )
                
                if employee_id:
                    created_count += 1
                else:
                    errors.append(f"Row {row_num}: Failed to create employee")
                    
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        return {
            "message": f"CSV upload completed. {created_count} employees created.",
            "created_count": created_count,
            "errors": errors
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CSV upload error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# User endpoints
@app.post("/user/login", response_model=dict)
async def user_login(request: LoginRequest):
    """User login - sends OTP (email + role)"""
    try:
        logger.info(f"🔍 User login request for email: {request.email}, role: {request.role}")
        
        # Validate role
        if request.role not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'user'")
        
        # Look up user by email and role
        user = get_user_by_email_and_role(request.email, request.role)
        logger.info(f"📋 User found: {user}")
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found with email {request.email} and role {request.role}")
        if not user["is_active"]:
            raise HTTPException(status_code=403, detail="User account is deactivated")
        
        # Generate and store OTP
        otp = generate_otp()
        expiry = get_otp_expiry()
        update_user_otp(user["id"], otp, expiry)
        
        # Send OTP email
        company = get_company_by_id(user["company_id"])
        success = send_otp_email(request.email, otp, company["name"] if company else "Your Company")
        if success:
            logger.info(f"✅ OTP sent successfully for {request.email} with role {request.role}")
            return {"message": "OTP sent successfully", "email": request.email, "role": request.role}
        else:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/user/verify-otp", response_model=TokenResponse)
async def user_verify_otp(request: OTPVerifyRequest):
    """User OTP verification (email + otp + role)"""
    try:
        logger.info(f"🔍 User verify OTP called for email: {request.email}, role: {request.role}")
        
        # Validate role
        if request.role not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'user'")
        
        # Look up user by email and role
        user = get_user_by_email_and_role(request.email, request.role)
        logger.info(f"📋 User found: {user}")
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found with email {request.email} and role {request.role}")
        if not user["is_active"]:
            raise HTTPException(status_code=403, detail="User account is deactivated")
        
        logger.info(f"🎯 User role from database: {user['role']}")
        
        # Verify OTP
        if not user["otp"] or user["otp"] != request.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        # Check OTP expiry
        if not user["otp_expiry"] or user["otp_expiry"] < datetime.utcnow():
            raise HTTPException(status_code=400, detail="OTP has expired")
        
        # Clear OTP after successful verification
        clear_user_otp(user["id"])
        
        # Create access token
        token_data = {
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "company_id": user["company_id"]
        }
        logger.info(f"🔐 Token data: {token_data}")
        access_token = create_access_token(token_data)
        
        response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(**user)
        )
        
        logger.info(f"✅ User verify OTP response: user role = {response.user.role}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User OTP verification error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/user/profile", response_model=UserResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    try:
        user_id = current_user.get("user_id")
        # Get user details from database
        # For now, return current user data from token
        return UserResponse(
            id=user_id,
            email=current_user.get("email"),
            role=current_user.get("role"),
            company_id=current_user.get("company_id"),
            is_active=True,
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Get user profile error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Appointment endpoints
@app.post("/appointments", response_model=AppointmentResponse)
async def create_appointment_endpoint(
    appointment: AppointmentCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new appointment"""
    try:
        logger.info(f"🔍 Creating appointment for user: {current_user.get('email')}")
        logger.info(f"📋 Appointment data: {appointment.dict()}")
        
        company_id = current_user.get("company_id")
        if not company_id:
            logger.error(f"❌ No company_id found in token for user: {current_user}")
            raise HTTPException(status_code=400, detail="Company ID not found in token")
        
        logger.info(f"🏢 Using company_id: {company_id}")
        
        # Create appointment in database
        logger.info("💾 Creating appointment in database...")
        appointment_id = create_appointment(
            employee_name=appointment.employee_name,
            department=appointment.department,
            reason=appointment.reason or "",
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time,
            visitor_name=appointment.visitor_name,
            visitor_email=appointment.visitor_email,
            visitor_phone=appointment.visitor_phone or "",
            company_id=company_id,
            booking_method=appointment.booking_method
        )
        
        if not appointment_id:
            logger.error("❌ Database create_appointment returned None")
            raise HTTPException(status_code=500, detail="Failed to create appointment")
        
        logger.info(f"✅ Appointment created with ID: {appointment_id}")
        
        # Get the created appointment
        logger.info("📥 Retrieving created appointment...")
        appointment_data = get_appointment_by_id(appointment_id)
        if not appointment_data:
            logger.error(f"❌ Failed to retrieve appointment with ID: {appointment_id}")
            raise HTTPException(status_code=500, detail="Failed to retrieve created appointment")
        
        logger.info(f"✅ Appointment retrieved: {appointment_data}")
        
        # Send confirmation email with QR code
        try:
            logger.info("📧 Sending confirmation email...")
            email_sent = email_service.send_appointment_confirmation(appointment_data)
            if email_sent:
                mark_appointment_email_sent(appointment_id)
                mark_appointment_qr_sent(appointment_id)
                logger.info(f"✅ Appointment confirmation email sent for appointment {appointment_id}")
            else:
                logger.warning(f"⚠️ Failed to send appointment confirmation email for appointment {appointment_id}")
        except Exception as e:
            logger.error(f"❌ Error sending appointment confirmation email: {e}")
        
        # Convert to response model
        logger.info("🔄 Converting to AppointmentResponse...")
        try:
            # Convert date and time fields to string if needed
            if "appointment_date" in appointment_data and not isinstance(appointment_data["appointment_date"], str):
                appointment_data["appointment_date"] = str(appointment_data["appointment_date"])
            if "appointment_time" in appointment_data and not isinstance(appointment_data["appointment_time"], str):
                appointment_data["appointment_time"] = str(appointment_data["appointment_time"])
            
            response_data = AppointmentResponse(**appointment_data)
            logger.info(f"✅ AppointmentResponse created successfully")
            return response_data
        except Exception as e:
            logger.error(f"❌ Error creating AppointmentResponse: {e}")
            logger.error(f"📋 Appointment data: {appointment_data}")
            raise HTTPException(status_code=500, detail=f"Error processing appointment data: {str(e)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Create appointment error: {e}")
        import traceback
        logger.error(f"📋 Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/appointments", response_model=List[AppointmentResponse])
async def get_appointments(current_user: dict = Depends(get_current_user)):
    """Get all appointments for the company"""
    try:
        company_id = current_user.get("company_id")
        if not company_id:
            raise HTTPException(status_code=400, detail="Company ID not found in token")
        
        logger.info(f"Fetching appointments for company_id: {company_id}")
        appointments = get_appointments_by_company(company_id)
        logger.info(f"Found {len(appointments)} appointments")
        
        # Convert to AppointmentResponse models with detailed error handling
        response_appointments = []
        for i, appointment in enumerate(appointments):
            try:
                # Convert date and time fields to string if needed
                if "appointment_date" in appointment and not isinstance(appointment["appointment_date"], str):
                    appointment["appointment_date"] = str(appointment["appointment_date"])
                if "appointment_time" in appointment and not isinstance(appointment["appointment_time"], str):
                    appointment["appointment_time"] = str(appointment["appointment_time"])
                response_appointment = AppointmentResponse(**appointment)
                response_appointments.append(response_appointment)
            except Exception as e:
                logger.error(f"Error converting appointment {i} to response model: {e}")
                logger.error(f"Appointment data: {appointment}")
                raise HTTPException(status_code=500, detail=f"Error processing appointment data: {str(e)}")
        
        return response_appointments
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get appointments error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get specific appointment by ID"""
    try:
        company_id = current_user.get("company_id")
        if not company_id:
            raise HTTPException(status_code=400, detail="Company ID not found in token")
        
        appointment = get_appointment_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        # Check if appointment belongs to user's company
        if appointment["company_id"] != company_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return AppointmentResponse(**appointment)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get appointment error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/appointments/{appointment_id}/status", response_model=AppointmentResponse)
async def update_appointment_status_endpoint(
    appointment_id: int,
    status_update: AppointmentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update appointment status"""
    try:
        company_id = current_user.get("company_id")
        if not company_id:
            raise HTTPException(status_code=400, detail="Company ID not found in token")
        
        # Check if appointment exists and belongs to user's company
        appointment = get_appointment_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        if appointment["company_id"] != company_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Update status
        success = update_appointment_status(appointment_id, status_update.status)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update appointment status")
        
        # Get updated appointment
        updated_appointment = get_appointment_by_id(appointment_id)
        return AppointmentResponse(**updated_appointment)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update appointment status error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/appointments/visitor/{visitor_email}", response_model=List[AppointmentResponse])
async def get_visitor_appointments(visitor_email: str):
    """Get appointments for a visitor by email (public endpoint)"""
    try:
        appointments = get_appointments_by_visitor_email(visitor_email)
        return [AppointmentResponse(**appointment) for appointment in appointments]
        
    except Exception as e:
        logger.error(f"Get visitor appointments error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Employee endpoints for users (authenticated but not admin-only)
@app.get("/employees", response_model=List[EmployeeResponse])
async def get_company_employees(current_user: dict = Depends(get_current_user)):
    """Get employees for the user's company (for booking purposes)"""
    try:
        company_id = current_user.get("company_id")
        if not company_id:
            raise HTTPException(status_code=400, detail="Company ID not found in token")
        
        # Get employees for the user's company
        employees = get_employees_by_company(company_id)
        
        return [EmployeeResponse(**employee) for employee in employees]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get company employees error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Voice Assistant SaaS API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 