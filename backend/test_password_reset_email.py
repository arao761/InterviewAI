"""
Test script to send a password reset email and verify it works.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.email_service import get_email_service
from app.core.logging import logger

def test_password_reset_email():
    """Test sending a password reset email."""
    print("=" * 60)
    print("Testing Password Reset Email")
    print("=" * 60)
    
    email_service = get_email_service()
    
    # Test email (use your actual email)
    test_email = input("Enter your email address to test: ").strip()
    test_name = "Test User"
    test_token = email_service.generate_verification_token()
    
    print(f"\nSending test email to: {test_email}")
    print(f"Reset token: {test_token}")
    print(f"Reset URL: {email_service.frontend_url}/reset-password?token={test_token}")
    print("\nAttempting to send email...")
    
    try:
        success = email_service.send_password_reset_email(
            email=test_email,
            name=test_name,
            token=test_token
        )
        
        if success:
            print("\n✅ Email sent successfully!")
            print(f"Check your inbox (and spam folder) at: {test_email}")
            print(f"\nIf you don't receive it, the reset URL is:")
            print(f"{email_service.frontend_url}/reset-password?token={test_token}")
        else:
            print("\n❌ Email failed to send. Check backend logs for details.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_reset_email()
