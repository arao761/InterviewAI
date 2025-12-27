#!/usr/bin/env python3
"""
Reset a user's password in the database.

Usage: python3 reset_user_password.py <email> <new_password>
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.models import User
from app.utils.auth import get_password_hash

def reset_password(email: str, new_password: str):
    """Reset a user's password."""
    db = SessionLocal()
    try:
        # Find user by email (case-insensitive)
        user = db.query(User).filter(User.email.ilike(email.lower().strip())).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found in database.")
            print("\nAvailable users:")
            users = db.query(User).all()
            for u in users:
                print(f"  - {u.email} (ID: {u.id})")
            return False
        
        # Hash new password
        hashed_password = get_password_hash(new_password)
        
        # Update user
        user.hashed_password = hashed_password
        db.commit()
        
        print(f"✅ Password reset successfully for user: {user.email}")
        print(f"   User ID: {user.id}")
        print(f"   Name: {user.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 reset_user_password.py <email> <new_password>")
        print("\nExample:")
        print("  python3 reset_user_password.py user@example.com MyNewPassword123")
        sys.exit(1)
    
    email = sys.argv[1]
    new_password = sys.argv[2]
    
    if len(new_password) < 8:
        print("❌ Password must be at least 8 characters long.")
        sys.exit(1)
    
    reset_password(email, new_password)

