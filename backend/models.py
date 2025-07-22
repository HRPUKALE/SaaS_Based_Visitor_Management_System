from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Superadmin models
class SuperadminLoginRequest(BaseModel):
    email: EmailStr

class SuperadminOTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

class SuperadminResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime

# Company models
class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    domain: Optional[str] = None
    max_users: Optional[int] = 100

class CompanyResponse(BaseModel):
    id: int
    name: str
    email: str
    domain: Optional[str]
    max_users: int
    is_active: bool
    created_by: int
    created_by_name: Optional[str] = None
    created_at: datetime

# User models
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    company_id: int
    company_name: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime

# Admin models
class AdminLoginRequest(BaseModel):
    email: EmailStr
    role: str  # 'admin' or 'user'

class AdminOTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
    role: str  # 'admin' or 'user'

# User login models
class LoginRequest(BaseModel):
    email: EmailStr
    role: str  # 'admin' or 'user'

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
    role: str  # 'admin' or 'user'

# Token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Health check
class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime

# Employee models
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    designation: Optional[str] = None
    phone: Optional[str] = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    designation: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime

# Appointment models
class AppointmentCreate(BaseModel):
    employee_name: str
    department: str
    reason: Optional[str] = None
    appointment_date: str
    appointment_time: str
    visitor_name: str
    visitor_email: EmailStr
    visitor_phone: Optional[str] = None
    booking_method: str = 'manual'

class AppointmentResponse(BaseModel):
    id: int
    employee_name: str
    department: str
    reason: Optional[str]
    appointment_date: str
    appointment_time: str
    visitor_name: str
    visitor_email: str
    visitor_phone: Optional[str]
    company_id: int
    company_name: Optional[str] = None
    booking_method: str
    status: str
    qr_code_sent: bool
    email_sent: bool
    created_at: datetime
    updated_at: datetime

class AppointmentUpdate(BaseModel):
    status: str

class AppointmentListResponse(BaseModel):
    appointments: List[AppointmentResponse]
    total: int 