#!/usr/bin/env python3
"""
Manually verify a user's email without needing the verification email.
Useful when SMTP is not configured or emails aren't being sent.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import User

def manually_verify_user(email: str):
    """Manually verify a user's email address."""
    db: Session = SessionLocal()
    try:
        # Find user by email (case-insensitive)
        user = db.query(User).filter(User.email.ilike(email.lower().strip())).first()
        
        if not user:
            print(f"❌ User not found: {email}")
            return False
        
        if user.email_verified:
            print(f"✅ User {user.email} is already verified")
            return True
        
        # Manually verify the user
        user.email_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        db.commit()
        
        print(f"✅ Successfully verified user: {user.email}")
        print(f"   User ID: {user.id}")
        print(f"   Name: {user.name}")
        print(f"   Created at: {user.created_at}")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def list_unverified_users():
    """List all unverified users."""
    db: Session = SessionLocal()
    try:
        users = db.query(User).filter(User.email_verified == False).all()
        
        if not users:
            print("✅ No unverified users found")
            return
        
        print(f"\n📋 Found {len(users)} unverified user(s):\n")
        for user in users:
            print(f"  Email: {user.email}")
            print(f"  Name: {user.name}")
            print(f"  Created: {user.created_at}")
            if user.verification_token:
                print(f"  Token: {user.verification_token[:30]}...")
            print()
        
    except Exception as e:
        print(f"❌ Error listing users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manually_verify_user.py <email>     # Verify specific user")
        print("  python manually_verify_user.py --list      # List all unverified users")
        print("\nExample:")
        print("  python manually_verify_user.py Vaibym07@gmail.com")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_unverified_users()
    else:
        email = sys.argv[1]
        manually_verify_user(email)

