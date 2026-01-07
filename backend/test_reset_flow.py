#!/usr/bin/env python3
"""Test the reset password flow to diagnose issues"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import User
from app.services.email_service import get_email_service

# Create database connection
engine = create_engine('sqlite:///./app.db')
Session = sessionmaker(bind=engine)
db = Session()

# Get user with reset token
user = db.query(User).filter(User.email == 'ankrao26@gmail.com').first()

if user and user.reset_token:
    email_service = get_email_service()
    reset_url = f"{email_service.frontend_url}/reset-password?token={user.reset_token}"

    print(f"\n📧 User: {user.email}")
    print(f"🔑 Reset Token: {user.reset_token}")
    print(f"⏰ Token Expires: {user.reset_token_expires}")
    print(f"\n🔗 Reset URL that was sent:")
    print(f"   {reset_url}")
    print(f"\n⚙️  Configuration:")
    print(f"   Frontend URL: {email_service.frontend_url}")

    # Check for double slash
    if "//" in reset_url.replace("https://", "").replace("http://", ""):
        print(f"\n⚠️  WARNING: Double slash detected in URL!")
    else:
        print(f"\n✅ URL format looks correct")

    print(f"\n💡 When you click the reset link, the frontend sends a request to:")
    print(f"   Production: Your production backend URL")
    print(f"   Local: http://localhost:8000/api/v1/auth/reset-password")
    print(f"\n❓ Question: Is your production frontend configured to call:")
    print(f"   A) A production backend (different database than local)")
    print(f"   B) Your local backend (same database)")
else:
    print("No reset token found for user")

db.close()
