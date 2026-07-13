import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings
from pathlib import Path

class EmailService:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.jinja_env = Environment(loader=FileSystemLoader(str(self.template_dir)))
    
    def send_email(self, to_email: str, subject: str, template_name: str, context: dict):
        """Send an email using SMTP"""
        try:
            # Render template
            template = self.jinja_env.get_template(f"{template_name}.html")
            html_content = template.render(**context)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.SMTP_USER
            msg['To'] = to_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    def send_welcome_email(self, email: str, full_name: str):
        """Send welcome email"""
        return self.send_email(
            to_email=email,
            subject="Welcome to Novexium!",
            template_name="welcome",
            context={
                "full_name": full_name,
                "company_name": "Novexium"
            }
        )
    
    def send_verification_email(self, email: str, full_name: str, token: str):
        """Send email verification email"""
        verification_url = f"{settings.APP_URL}/auth/verify/{token}"
        
        return self.send_email(
            to_email=email,
            subject="Verify Your Email Address",
            template_name="verify_email",
            context={
                "full_name": full_name,
                "verification_url": verification_url,
                "company_name": "Novexium"
            }
        )
    
    def send_password_reset_email(self, email: str, full_name: str, token: str):
        """Send password reset email"""
        reset_url = f"{settings.APP_URL}/auth/reset-password/{token}"
        
        return self.send_email(
            to_email=email,
            subject="Reset Your Password",
            template_name="reset_password",
            context={
                "full_name": full_name,
                "reset_url": reset_url,
                "company_name": "Novexium"
            }
        )
