# Database Guide: Accessing User Information

## Database Location

The database is stored locally in your code directory:
- **Location**: `backend/app.db`
- **Type**: SQLite (file-based database)
- **No external database server needed** - it's just a file in your project!

## User Model Structure

Each user in the database has the following fields:

```python
{
    "id": 1,                    # Unique identifier (auto-incrementing)
    "email": "user@example.com", # User's email (unique, required)
    "name": "John Doe",         # User's name (required)
    "hashed_password": "...",   # Encrypted password (never expose this!)
    "created_at": "2025-12-23...", # When account was created
    "updated_at": "2025-12-23..."  # Last update timestamp
}
```

## How to Access User Data in Your Code

### Method 1: In FastAPI Routes (Recommended)

```python
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User

# Get all users
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

# Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}

# Get user by email
@app.get("/users/email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}
```

### Method 2: Direct Database Access

```python
from app.core.database import SessionLocal
from app.models.models import User

# Create a database session
db = SessionLocal()

try:
    # Get all users
    users = db.query(User).all()
    
    # Get user by email
    user = db.query(User).filter(User.email == "user@example.com").first()
    
    # Get user by ID
    user = db.query(User).filter(User.id == 1).first()
    
    # Count users
    count = db.query(User).count()
    
    # Search by name
    users = db.query(User).filter(User.name.contains("John")).all()
    
finally:
    db.close()  # Always close the session!
```

### Method 3: Using the Current User (Already Authenticated)

In routes that require authentication, you can get the current user directly:

```python
from app.api.routes.auth import get_current_user
from app.models.models import User

@app.get("/my-profile")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at
    }
```

## Common Queries

### Get All Users
```python
users = db.query(User).all()
```

### Get User by Email
```python
user = db.query(User).filter(User.email == "user@example.com").first()
```

### Get User by ID
```python
user = db.query(User).filter(User.id == 1).first()
```

### Count Users
```python
count = db.query(User).count()
```

### Search Users by Name
```python
users = db.query(User).filter(User.name.contains("John")).all()
```

### Get Users Created After Date
```python
from datetime import datetime
users = db.query(User).filter(User.created_at >= datetime(2025, 1, 1)).all()
```

## Example: Complete User Access Script

See `backend/examples/access_user_data.py` for a complete working example with all these patterns.

## Important Notes

1. **Never expose passwords**: The `hashed_password` field is encrypted. Never return it in API responses.

2. **Always close sessions**: When using `SessionLocal()` directly, always close it with `db.close()` in a `finally` block.

3. **Use dependencies in FastAPI**: In FastAPI routes, use `Depends(get_db)` - it automatically handles session management.

4. **Database file location**: The database file `app.db` is in the `backend/` directory. You can view it with SQLite tools if needed.

## Viewing the Database Directly

You can view the database using SQLite command line:

```bash
cd backend
sqlite3 app.db
.tables          # Show all tables
.schema users    # Show users table structure
SELECT * FROM users;  # View all users
```

Or use a GUI tool like DB Browser for SQLite.

