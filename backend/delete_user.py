#!/usr/bin/env python3
"""
Delete a user account from the database.

Usage: python3 delete_user.py <email>
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.models import User

def delete_user(email: str):
    """Delete a user account."""
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
        
        # Confirm deletion
        print(f"\n⚠️  WARNING: This will permanently delete the following user:")
        print(f"   ID: {user.id}")
        print(f"   Name: {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Created: {user.created_at}")
        print(f"   Sessions: {len(user.sessions)}")
        print(f"   Payments: {len(user.payments)}")
        
        confirm = input(f"\nType 'DELETE' to confirm deletion: ")
        
        if confirm != 'DELETE':
            print("❌ Deletion cancelled.")
            return False
        
        # Delete user (cascade will handle related records)
        db.delete(user)
        db.commit()
        
        print(f"✅ User account deleted successfully: {user.email}")
        return True
        
    except Exception as e:
        print(f"❌ Error deleting user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 delete_user.py <email>")
        print("\nExample:")
        print("  python3 delete_user.py user@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    delete_user(email)

