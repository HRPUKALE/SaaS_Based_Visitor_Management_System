import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import qrcode
import qrcode.constants
import io
import base64
import logging
from typing import Optional, Dict, Any
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = EMAIL_PORT
        self.user = EMAIL_USER
        self.password = EMAIL_PASSWORD
        
        # Check if email is properly configured
        self.email_configured = bool(self.user and self.password)
        if not self.email_configured:
            print("⚠️  Warning: Email credentials not configured. Appointment emails will not be sent.")
            print("   To enable email notifications, set EMAIL_USER and EMAIL_PASSWORD in your .env file")
        
    def generate_qr_code(self, appointment_data: Dict[str, Any]) -> str:
        """Generate QR code for appointment and return as base64 string"""
        try:
            # Create QR code data
            qr_data = f"""
            Appointment ID: {appointment_data['id']}
            Employee: {appointment_data['employee_name']}
            Department: {appointment_data['department']}
            Date: {appointment_data['appointment_date']}
            Time: {appointment_data['appointment_time']}
            Visitor: {appointment_data['visitor_name']}
            Company: {appointment_data['company_name']}
            """
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer)
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return img_base64
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            return ""
    
    def send_appointment_confirmation(self, appointment_data: Dict[str, Any]) -> bool:
        """Send appointment confirmation email with QR code"""
        try:
            # Check if email is configured
            if not self.email_configured:
                logger.warning("Email not configured. Skipping appointment confirmation email.")
                return True  # Return True to not block appointment creation
            
            # Generate QR code
            qr_code_base64 = self.generate_qr_code(appointment_data)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Appointment Confirmation - {appointment_data['company_name']}"
            msg['From'] = self.user
            msg['To'] = appointment_data['visitor_email']
            
            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Appointment Confirmation</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .appointment-details {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                    .qr-section {{ text-align: center; margin: 20px 0; }}
                    .qr-code {{ border: 2px solid #ddd; padding: 10px; display: inline-block; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                    .detail-row {{ margin: 10px 0; }}
                    .label {{ font-weight: bold; color: #555; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Appointment Confirmation</h1>
                        <p>Your appointment has been successfully scheduled</p>
                    </div>
                    
                    <div class="content">
                        <div class="appointment-details">
                            <h2>Appointment Details</h2>
                            
                            <div class="detail-row">
                                <span class="label">Appointment ID:</span>
                                <span>{appointment_data['id']}</span>
                            </div>
                            
                            <div class="detail-row">
                                <span class="label">Employee:</span>
                                <span>{appointment_data['employee_name']}</span>
                            </div>
                            
                            <div class="detail-row">
                                <span class="label">Department:</span>
                                <span>{appointment_data['department']}</span>
                            </div>
                            
                            <div class="detail-row">
                                <span class="label">Date:</span>
                                <span>{appointment_data['appointment_date']}</span>
                            </div>
                            
                            <div class="detail-row">
                                <span class="label">Time:</span>
                                <span>{appointment_data['appointment_time']}</span>
                            </div>
                            
                            <div class="detail-row">
                                <span class="label">Visitor Name:</span>
                                <span>{appointment_data['visitor_name']}</span>
                            </div>
                            
                            <div class="detail-row">
                                <span class="label">Company:</span>
                                <span>{appointment_data['company_name']}</span>
                            </div>
                            
                            {f'<div class="detail-row"><span class="label">Reason:</span><span>{appointment_data["reason"]}</span></div>' if appointment_data.get('reason') else ''}
                        </div>
                        
                        <div class="qr-section">
                            <h3>Your QR Code</h3>
                            <p>Please present this QR code at the reception desk when you arrive:</p>
                            <div class="qr-code">
                                <img src="data:image/png;base64,{qr_code_base64}" alt="Appointment QR Code" style="max-width: 200px;">
                            </div>
                        </div>
                        
                        <div style="margin: 20px 0; padding: 15px; background-color: #e7f3ff; border-left: 4px solid #2196F3;">
                            <h4>Important Information:</h4>
                            <ul>
                                <li>Please arrive 10 minutes before your scheduled appointment time</li>
                                <li>Bring a valid ID for verification</li>
                                <li>If you need to reschedule or cancel, please contact us as soon as possible</li>
                                <li>This QR code is unique to your appointment and should not be shared</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>Thank you for choosing {appointment_data['company_name']}</p>
                        <p>This is an automated message, please do not reply to this email</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Create plain text content
            text_content = f"""
            Appointment Confirmation
            
            Your appointment has been successfully scheduled with {appointment_data['company_name']}.
            
            Appointment Details:
            - Appointment ID: {appointment_data['id']}
            - Employee: {appointment_data['employee_name']}
            - Department: {appointment_data['department']}
            - Date: {appointment_data['appointment_date']}
            - Time: {appointment_data['appointment_time']}
            - Visitor Name: {appointment_data['visitor_name']}
            {f"- Reason: {appointment_data['reason']}" if appointment_data.get('reason') else ""}
            
            Please arrive 10 minutes before your scheduled appointment time and bring a valid ID for verification.
            
            Thank you for choosing {appointment_data['company_name']}.
            """
            
            # Attach parts
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
                server.login(self.user, self.password)
                server.sendmail(self.user, appointment_data['visitor_email'], msg.as_string())
            
            logger.info(f"Appointment confirmation email sent to {appointment_data['visitor_email']}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending appointment confirmation email: {e}")
            return False
    
    def send_appointment_reminder(self, appointment_data: Dict[str, Any]) -> bool:
        """Send appointment reminder email"""
        try:
            # Check if email is configured
            if not self.email_configured:
                logger.warning("Email not configured. Skipping appointment reminder email.")
                return True  # Return True to not block the process
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Appointment Reminder - {appointment_data['company_name']}"
            msg['From'] = self.user
            msg['To'] = appointment_data['visitor_email']
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Appointment Reminder</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #FF9800; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .reminder {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Appointment Reminder</h1>
                        <p>Your appointment is tomorrow</p>
                    </div>
                    
                    <div class="content">
                        <div class="reminder">
                            <h2>Appointment Details</h2>
                            <p><strong>Employee:</strong> {appointment_data['employee_name']}</p>
                            <p><strong>Department:</strong> {appointment_data['department']}</p>
                            <p><strong>Date:</strong> {appointment_data['appointment_date']}</p>
                            <p><strong>Time:</strong> {appointment_data['appointment_time']}</p>
                            <p><strong>Company:</strong> {appointment_data['company_name']}</p>
                            
                            <p style="margin-top: 20px; padding: 15px; background-color: #fff3cd; border-left: 4px solid #ffc107;">
                                <strong>Reminder:</strong> Please arrive 10 minutes before your scheduled appointment time and bring a valid ID for verification.
                            </p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            part = MIMEText(html_content, 'html')
            msg.attach(part)
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
                server.login(self.user, self.password)
                server.sendmail(self.user, appointment_data['visitor_email'], msg.as_string())
            
            logger.info(f"Appointment reminder email sent to {appointment_data['visitor_email']}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending appointment reminder email: {e}")
            return False

# Global email service instance
email_service = EmailService() 