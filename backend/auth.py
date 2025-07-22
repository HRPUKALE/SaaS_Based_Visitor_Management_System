import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import random
import string
from config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, OTP_EXPIRE_MINUTES
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD

def create_access_token(data: Dict[str, Any]) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def get_otp_expiry() -> str:
    """Get OTP expiry timestamp"""
    expiry = datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    return expiry.strftime('%Y-%m-%d %H:%M:%S')

def send_otp_email(email: str, otp: str, company_name: str) -> bool:
    """Send OTP email to user"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = f"Login OTP - {company_name} Voice Assistant"
        
        body = f"""
        Hello,
        
        Your login OTP for {company_name} Voice Assistant is: {otp}
        
        This OTP will expire in {OTP_EXPIRE_MINUTES} minutes.
        
        If you didn't request this OTP, please ignore this email.
        
        Best regards,
        {company_name} Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False

def send_otp_email_mock(email: str, otp: str, company_name: str) -> bool:
    """Mock email sending for development (prints OTP to console)"""
    print(f"\n{'='*50}")
    print(f"OTP Email to: {email}")
    print(f"Company: {company_name}")
    print(f"OTP: {otp}")
    print(f"Expires in: {OTP_EXPIRE_MINUTES} minutes")
    print(f"{'='*50}\n")
    return True 