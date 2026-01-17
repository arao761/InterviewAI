"""
Email service for sending verification emails and other notifications.
"""
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.core.config import settings
from app.core.logging import logger

# AWS SES support
try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


class EmailService:
    """Service for sending emails."""

    def __init__(self):
        # AWS SES configuration (preferred for production)
        self.aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', '').strip()
        self.aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '').strip()
        self.aws_region = getattr(settings, 'AWS_REGION', 'us-east-1').strip()
        self.aws_ses_from_email = getattr(settings, 'AWS_SES_FROM_EMAIL', '').strip()

        # SMTP configuration (fallback for local development)
        self.smtp_host = getattr(settings, 'SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'SMTP_PORT', 587)
        self.smtp_user = getattr(settings, 'SMTP_USER', '').strip()
        # Strip password to remove any whitespace/newlines that might cause auth issues
        smtp_password_raw = getattr(settings, 'SMTP_PASSWORD', '')
        self.smtp_password = smtp_password_raw.strip().replace(' ', '') if smtp_password_raw else ''
        self.from_email = getattr(settings, 'FROM_EMAIL', self.smtp_user).strip()
        self.frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')

        # Determine which email method to use
        self.use_ses = HAS_BOTO3 and bool(self.aws_access_key and self.aws_secret_key)

        if self.use_ses:
            logger.info("Email service initialized with AWS SES")
            self.ses_client = boto3.client(
                'ses',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
        else:
            logger.info("Email service initialized with SMTP")
        
    def generate_verification_token(self) -> str:
        """Generate a secure random token for email verification."""
        return secrets.token_urlsafe(32)

    def _send_via_ses(self, to_email: str, subject: str, html_body: str, text_body: str) -> bool:
        """Send email via AWS SES."""
        try:
            response = self.ses_client.send_email(
                Source=self.aws_ses_from_email,
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': {
                        'Text': {'Data': text_body, 'Charset': 'UTF-8'},
                        'Html': {'Data': html_body, 'Charset': 'UTF-8'}
                    }
                }
            )
            logger.info(f"✅ Email sent via SES to {to_email}. MessageId: {response['MessageId']}")
            return True
        except ClientError as e:
            logger.error(f"SES error sending email to {to_email}: {e.response['Error']['Message']}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email via SES to {to_email}: {e}")
            return False

    def send_verification_email(self, email: str, name: str, token: str) -> bool:
        """
        Send email verification email.
        
        Args:
            email: User's email address
            name: User's name
            token: Verification token
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Check if any email method is configured
            if not self.use_ses and (not self.smtp_user or not self.smtp_password):
                logger.warning("No email service configured - email verification disabled.")
                logger.info(f"Verification token for {email}: {token}")
                logger.info(f"Verification URL: {self.frontend_url}/verify-email?token={token}")
                return False

            # Create verification URL
            verification_url = f"{self.frontend_url}/verify-email?token={token}"

            # Create HTML email body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4F46E5; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                    .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 5px 5px; }}
                    .button {{ display: inline-block; padding: 12px 24px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to InterviewAI!</h1>
                    </div>
                    <div class="content">
                        <p>Hi {name},</p>
                        <p>Thank you for signing up for InterviewAI. Please verify your email address by clicking the button below:</p>
                        <p style="text-align: center;">
                            <a href="{verification_url}" class="button">Verify Email Address</a>
                        </p>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #4F46E5;">{verification_url}</p>
                        <p>This link will expire in 24 hours.</p>
                        <p>If you didn't create an account, please ignore this email.</p>
                    </div>
                    <div class="footer">
                        <p>© 2024 InterviewAI. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Create plain text version
            text_body = f"""
            Welcome to InterviewAI!
            
            Hi {name},
            
            Thank you for signing up for InterviewAI. Please verify your email address by visiting:
            
            {verification_url}
            
            This link will expire in 24 hours.
            
            If you didn't create an account, please ignore this email.
            
            © 2024 InterviewAI. All rights reserved.
            """

            # Send via AWS SES or SMTP
            if self.use_ses:
                return self._send_via_ses(
                    to_email=email,
                    subject='Verify Your Email - InterviewAI',
                    html_body=html_body,
                    text_body=text_body
                )

            # Fall back to SMTP
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Verify Your Email - InterviewAI'
            msg['From'] = self.from_email
            msg['To'] = email

            # Attach both versions
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))

            # Send email with explicit envelope to ensure it goes to the user, not the sender
            logger.info(f"Attempting to send verification email to {email} via SMTP {self.smtp_host}:{self.smtp_port}")
            logger.info(f"Using SMTP user: {self.smtp_user}, From: {self.from_email}")
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                logger.info(f"Connected to SMTP server {self.smtp_host}:{self.smtp_port}")
                server.starttls()
                logger.info("TLS started successfully")
                server.login(self.smtp_user, self.smtp_password)
                logger.info(f"SMTP login successful for {self.smtp_user}")
                # Use sendmail with explicit envelope to ensure recipient is correct
                server.sendmail(
                    from_addr=self.from_email,  # Envelope sender (Interview AI)
                    to_addrs=[email],  # Envelope recipient (user who registered)
                    msg=msg.as_string()
                )
                logger.info(f"Email message sent via SMTP to {email}")
            
            logger.info(f"✅ Verification email sent successfully to {email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed for {email}: {e}")
            logger.error(f"Check SMTP_USER and SMTP_PASSWORD. Error code: {e.smtp_code}, Error message: {e.smtp_error}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email to {email}: {e}")
            logger.error(f"SMTP error code: {getattr(e, 'smtp_code', 'N/A')}, Error: {getattr(e, 'smtp_error', str(e))}")
            return False
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return False
    
    def send_password_reset_email(self, email: str, name: str, token: str) -> bool:
        """
        Send password reset email.
        
        Args:
            email: User's email address
            name: User's name
            token: Password reset token
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Check if any email method is configured
            if not self.use_ses and (not self.smtp_user or not self.smtp_password):
                logger.warning("No email service configured - password reset email disabled.")
                logger.info(f"Password reset token for {email}: {token}")
                return False

            # tokens from secrets.token_urlsafe() are already URL-safe (base64url encoding)
            # They contain only: A-Z, a-z, 0-9, -, _ which are all safe in URLs
            # No need to URL-encode them - use token directly
            reset_url = f"{self.frontend_url}/reset-password?token={token}"
            logger.info(f"Password reset URL generated for {email} - token length: {len(token)}")

            html_body = f"""
            <!DOCTYPE html>
            <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2>Password Reset Request</h2>
                    <p>Hi {name},</p>
                    <p>You requested to reset your password. Click the button below to reset it:</p>
                    <p><a href="{reset_url}" style="display: inline-block; padding: 12px 24px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
                    <p>Or copy this link: {reset_url}</p>
                    <p>This link will expire in 1 hour.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                </div>
            </body>
            </html>
            """

            text_body = f"""
            Password Reset Request

            Hi {name},

            You requested to reset your password. Visit this link to reset it:

            {reset_url}

            This link will expire in 1 hour.

            If you didn't request this, please ignore this email.

            © 2024 InterviewAI. All rights reserved.
            """

            # Send via AWS SES or SMTP
            if self.use_ses:
                return self._send_via_ses(
                    to_email=email,
                    subject='Reset Your Password - InterviewAI',
                    html_body=html_body,
                    text_body=text_body
                )

            # Fall back to SMTP
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Reset Your Password - InterviewAI'
            # Gmail requires FROM to match authenticated user, so use smtp_user
            msg['From'] = self.smtp_user
            msg['To'] = email
            msg['Reply-To'] = self.from_email if self.from_email != self.smtp_user else self.smtp_user

            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))

            # Send email with explicit envelope to ensure it goes to the user, not the sender
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                # Use sendmail with explicit envelope - FROM must match authenticated user
                server.sendmail(
                    from_addr=self.smtp_user,  # Must match authenticated user for Gmail
                    to_addrs=[email],  # Envelope recipient (user who requested reset)
                    msg=msg.as_string()
                )
            
            logger.info(f"Password reset email sent to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return False


# Singleton instance
_email_service: Optional[EmailService] = None

def get_email_service() -> EmailService:
    """Get or create email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service

