#!/usr/bin/env python3
"""
Get verification token for a user so you can manually construct the verification URL.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import User
from app.services.email_service import get_email_service

def get_verification_info(email: str):
    """Get verification token and URL for a user."""
    db: Session = SessionLocal()
    try:
        # Find user by email (case-insensitive)
        user = db.query(User).filter(User.email.ilike(email.lower().strip())).first()
        
        if not user:
            print(f"❌ User not found: {email}")
            return
        
        if user.email_verified:
            print(f"✅ User {user.email} is already verified")
            return
        
        if not user.verification_token:
            print(f"❌ No verification token found for {user.email}")
            print("   The user may need to register again or request a new verification email.")
            return
        
        # Get frontend URL from email service
        email_service = get_email_service()
        verification_url = f"{email_service.frontend_url}/verify-email?token={user.verification_token}"
        
        print(f"\n📧 User: {user.email}")
        print(f"👤 Name: {user.name}")
        print(f"🔑 Verification Token: {user.verification_token}")
        print(f"⏰ Token Expires: {user.verification_token_expires}")
        print(f"\n🔗 Verification URL:")
        print(f"   {verification_url}")
        print(f"\n💡 You can:")
        print(f"   1. Copy the URL above and open it in your browser")
        print(f"   2. Or use the token with the API: POST /api/v1/auth/verify-email")
        print(f"      Body: {{\"token\": \"{user.verification_token}\"}}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_verification_token.py <email>")
        print("\nExample:")
        print("  python get_verification_token.py Vaibym07@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    get_verification_info(email)

