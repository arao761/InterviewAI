#!/usr/bin/env python3
"""
Manually verify a user's email in the database.

Usage: python3 manually_verify_user.py <email>
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.models import User

def verify_user(email: str):
    """Verify a user's email."""
    db = SessionLocal()
    try:
        # Find user by email (case-insensitive)
        user = db.query(User).filter(User.email.ilike(email.lower().strip())).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found in database.")
            print("\nAvailable users:")
            users = db.query(User).all()
            for u in users:
                print(f"  - {u.email} (ID: {u.id}, Verified: {u.email_verified})")
            return False
        
        # Update user verification status
        user.email_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        db.commit()
        
        print(f"✅ Email verified successfully for user: {user.email}")
        print(f"   User ID: {user.id}")
        print(f"   Name: {user.name}")
        print(f"   Verified: {user.email_verified}")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 manually_verify_user.py <email>")
        print("\nExample:")
        print("  python3 manually_verify_user.py ankrao26@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    verify_user(email)