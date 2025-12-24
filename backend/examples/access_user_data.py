"""
Example: How to Access User Data from the Database

This file shows you how to access user information stored in the local database.
The database is a SQLite file located at: backend/app.db
"""

from app.core.database import SessionLocal, get_db
from app.models.models import User
from sqlalchemy.orm import Session


# ============================================
# Example 1: Get all users
# ============================================
def get_all_users():
    """Get all users from the database."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"  - ID: {user.id}, Name: {user.name}, Email: {user.email}")
        return users
    finally:
        db.close()


# ============================================
# Example 2: Get a user by email
# ============================================
def get_user_by_email(email: str):
    """Get a specific user by their email address."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"Found user: {user.name} ({user.email})")
            print(f"  Created at: {user.created_at}")
            return user
        else:
            print(f"No user found with email: {email}")
            return None
    finally:
        db.close()


# ============================================
# Example 3: Get a user by ID
# ============================================
def get_user_by_id(user_id: int):
    """Get a specific user by their ID."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            print(f"User ID {user_id}: {user.name} ({user.email})")
            return user
        else:
            print(f"No user found with ID: {user_id}")
            return None
    finally:
        db.close()


# ============================================
# Example 4: Count total users
# ============================================
def count_users():
    """Count the total number of users in the database."""
    db = SessionLocal()
    try:
        count = db.query(User).count()
        print(f"Total number of users: {count}")
        return count
    finally:
        db.close()


# ============================================
# Example 5: Get user information (all fields)
# ============================================
def get_user_info(user_id: int):
    """Get complete user information."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            print("=" * 50)
            print(f"User Information for ID: {user_id}")
            print("=" * 50)
            print(f"ID: {user.id}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}")
            print(f"Created At: {user.created_at}")
            print(f"Updated At: {user.updated_at}")
            print(f"Number of Sessions: {len(user.sessions)}")
            print("=" * 50)
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "total_sessions": len(user.sessions)
            }
        else:
            print(f"User with ID {user_id} not found")
            return None
    finally:
        db.close()


# ============================================
# Example 6: Using in FastAPI route (with dependency)
# ============================================
"""
In your FastAPI routes, you can access user data like this:

from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}
"""


# ============================================
# Example 7: Search users by name
# ============================================
def search_users_by_name(search_term: str):
    """Search for users by name (case-insensitive partial match)."""
    db = SessionLocal()
    try:
        users = db.query(User).filter(
            User.name.ilike(f"%{search_term}%")
        ).all()
        print(f"Found {len(users)} user(s) matching '{search_term}':")
        for user in users:
            print(f"  - {user.name} ({user.email})")
        return users
    finally:
        db.close()


# ============================================
# Example 8: Get users created in date range
# ============================================
def get_users_by_date_range(start_date, end_date):
    """Get users created between two dates."""
    from datetime import datetime
    db = SessionLocal()
    try:
        users = db.query(User).filter(
            User.created_at >= start_date,
            User.created_at <= end_date
        ).all()
        print(f"Found {len(users)} user(s) created between {start_date} and {end_date}")
        return users
    finally:
        db.close()


# ============================================
# Main function to run examples
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("User Database Access Examples")
    print("=" * 60)
    print("\nDatabase Location: backend/app.db")
    print("\nUser Model Fields:")
    print("  - id: Integer (primary key)")
    print("  - email: String (unique)")
    print("  - name: String")
    print("  - hashed_password: String (encrypted)")
    print("  - created_at: DateTime")
    print("  - updated_at: DateTime")
    print("\n" + "=" * 60)
    
    # Run examples
    print("\n1. Counting users...")
    count_users()
    
    print("\n2. Getting all users...")
    get_all_users()
    
    print("\n3. Getting user by email...")
    get_user_by_email("test@example.com")
    
    print("\n4. Getting user by ID...")
    get_user_by_id(1)
    
    print("\n5. Getting complete user info...")
    get_user_info(1)
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

