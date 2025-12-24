#!/usr/bin/env python3
"""
Visual Database Viewer - Terminal/IDE Version

Run this script to see all users in the database in a nice table format.
Usage: python3 view_database.py

This displays the database directly in your terminal/IDE, not on a website.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.models import User
from datetime import datetime

def view_users_table():
    """Display all users in a formatted table."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        if not users:
            print("\n" + "=" * 90)
            print("No users found in the database.")
            print("=" * 90)
            return
        
        # Print header
        print("\n" + "=" * 90)
        print(" " * 30 + "DATABASE VIEWER - USERS TABLE")
        print("=" * 90)
        print(f"Database Location: backend/app.db")
        print(f"Total Users: {len(users)}")
        print(f"View Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 90)
        print()
        
        # Print table header
        print(f"{'ID':<6} {'Name':<30} {'Email':<35} {'Created At':<20}")
        print("-" * 90)
        
        # Print each user
        for user in users:
            created_at = user.created_at.strftime("%Y-%m-%d %H:%M") if user.created_at else "N/A"
            name = user.name[:28] + ".." if len(user.name) > 30 else user.name
            email = user.email[:33] + ".." if len(user.email) > 35 else user.email
            
            print(f"{user.id:<6} {name:<30} {email:<35} {created_at:<20}")
        
        print("-" * 90)
        print(f"Total: {len(users)} user(s)")
        print("=" * 90)
        print()
        
        # Print detailed info
        print("\nDetailed User Information:")
        print("=" * 90)
        for user in users:
            print(f"\nUser ID: {user.id}")
            print(f"  Name: {user.name}")
            print(f"  Email: {user.email}")
            print(f"  Created: {user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'N/A'}")
            print(f"  Updated: {user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else 'N/A'}")
            print(f"  Sessions: {len(user.sessions)}")
        
        print("\n" + "=" * 90)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you're running this from the backend directory:")
        print("  cd backend")
        print("  source ../venv/bin/activate")
        print("  python3 view_database.py")
    finally:
        db.close()


if __name__ == "__main__":
    view_users_table()

