"""
Authentication routes for user registration and login.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.auth_schemas import UserRegister, UserLogin, Token, UserResponse
from app.utils.auth import verify_password, get_password_hash, create_access_token, decode_access_token
from app.core.logging import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.

    - Creates a new user account with hashed password
    - Returns user information (excluding password)
    """
    try:
        # Debug logging
        logger.info(f"Registration attempt - Email: {user_data.email}, Password length: {len(user_data.password)} chars, {len(user_data.password.encode('utf-8'))} bytes")

        # Normalize email to lowercase for consistency
        email_lower = user_data.email.lower().strip()
        
        logger.info(f"Registration attempt for email: {email_lower}")
        
        # Check if user already exists (case-insensitive)
        existing_user = db.query(User).filter(User.email.ilike(email_lower)).first()
        if existing_user:
            logger.warning(f"Registration failed - Email already exists: {existing_user.email} (ID: {existing_user.id})")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        logger.info(f"No existing user found for: {email_lower}, proceeding with registration")

        # Validate password length in bytes
        password_bytes = len(user_data.password.encode('utf-8'))
        if password_bytes > 72:
            logger.error(f"Password too long: {password_bytes} bytes")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password is too long ({password_bytes} bytes). Maximum is 72 bytes."
            )

        # Create new user with hashed password (store email in lowercase)
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=email_lower,
            name=user_data.name,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"New user registered: {new_user.email}")
        return new_user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.

    - Validates credentials
    - Returns JWT access token
    """
    try:
        # Normalize email to lowercase for case-insensitive matching
        email_lower = credentials.email.lower().strip()
        
        # Find user by email (case-insensitive)
        user = db.query(User).filter(User.email.ilike(email_lower)).first()
        
        if not user:
            logger.warning(f"Login attempt failed - User not found: {email_lower}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.hashed_password:
            logger.warning(f"Login attempt failed - No password hash for user: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password with detailed logging
        logger.info(f"Attempting password verification for user: {user.email}")
        logger.info(f"Password length received: {len(credentials.password)} chars, {len(credentials.password.encode('utf-8'))} bytes")
        logger.info(f"Stored hash starts with: {user.hashed_password[:20] if user.hashed_password else 'None'}...")
        password_valid = verify_password(credentials.password, user.hashed_password)
        logger.info(f"Password verification result: {password_valid}")
        
        if not password_valid:
            logger.warning(f"Login attempt failed - Invalid password for user: {user.email}")
            logger.warning(f"Received password: '{credentials.password}' (length: {len(credentials.password)})")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )

        logger.info(f"User logged in: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Usage:
        @router.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.email}
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Requires: Valid JWT token in Authorization header
    """
    return current_user


