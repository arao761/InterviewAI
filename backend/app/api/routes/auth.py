"""
Authentication routes for user registration and login.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.auth_schemas import UserRegister, UserLogin, Token, UserResponse, VerifyEmailRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.utils.auth import verify_password, get_password_hash, create_access_token, decode_access_token
from app.core.logging import logger
from app.services.email_service import get_email_service
from datetime import datetime, timedelta, timezone

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
        
        # Generate verification token and set expiration (24 hours from now)
        email_service = get_email_service()
        verification_token = email_service.generate_verification_token()
        verification_token_expires = datetime.now(timezone.utc) + timedelta(hours=24)
        
        # Create new user - email NOT verified initially (requires verification)
        new_user = User(
            email=email_lower,
            name=user_data.name,
            hashed_password=hashed_password,
            email_verified=False,  # Requires email verification
            verification_token=verification_token,
            verification_token_expires=verification_token_expires
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Send verification email
        email_sent = email_service.send_verification_email(
            email=email_lower,
            name=user_data.name,
            token=verification_token
        )
        
        if email_sent:
            logger.info(f"New user registered: {new_user.email} - Verification email sent")
        else:
            logger.warning(f"New user registered: {new_user.email} - Verification email NOT sent (SMTP not configured)")
            logger.info(f"Verification token for {email_lower}: {verification_token}")
            logger.info(f"Verification URL: {email_service.frontend_url}/verify-email?token={verification_token}")

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

        # Check if email is verified
        if not user.email_verified:
            logger.warning(f"Login attempt failed - Email not verified for user: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email address before logging in. Check your inbox for the verification email.",
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


@router.post("/verify-email")
async def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    """
    Verify user email with verification token (legacy endpoint - emails are auto-verified now).
    
    Args:
        request: Request body containing token
        
    Returns:
        Success message
    """
    try:
        token = request.token
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token is required"
            )
        
        # Find user by verification token
        user = db.query(User).filter(User.verification_token == token).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        # Check if token is expired
        if user.verification_token_expires:
            # Ensure both datetimes are timezone-aware for comparison
            expires = user.verification_token_expires
            if expires.tzinfo is None:
                # If database returned naive datetime, assume UTC
                expires = expires.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            if expires < now:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Verification token has expired. Please request a new one."
                )
        
        # Mark as verified (for backwards compatibility with old tokens)
        user.email_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        db.commit()
        
        logger.info(f"Email verified for user: {user.email}")
        return {"message": "Email verified successfully", "email_verified": True}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )


@router.post("/resend-verification")
async def resend_verification_email(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Resend verification email to user.
    
    Args:
        request: Request body containing email
        
    Returns:
        Success message
    """
    try:
        email_lower = request.email.lower().strip()
        
        # Find user by email
        user = db.query(User).filter(User.email.ilike(email_lower)).first()
        
        if not user:
            # Don't reveal if email exists or not (security best practice)
            logger.info(f"Resend verification requested for non-existent email: {email_lower}")
            return {"message": "If an account exists with this email, a verification email has been sent."}
        
        # Check if already verified
        if user.email_verified:
            logger.info(f"Resend verification requested for already verified email: {email_lower}")
            return {"message": "This email is already verified. You can log in."}
        
        # Generate new verification token
        email_service = get_email_service()
        verification_token = email_service.generate_verification_token()
        verification_token_expires = datetime.now(timezone.utc) + timedelta(hours=24)
        
        # Update user with new token
        user.verification_token = verification_token
        user.verification_token_expires = verification_token_expires
        db.commit()
        
        # Send verification email
        email_sent = email_service.send_verification_email(
            email=email_lower,
            name=user.name,
            token=verification_token
        )
        
        if email_sent:
            logger.info(f"Verification email resent to {email_lower}")
            return {"message": "Verification email sent. Please check your inbox."}
        else:
            logger.warning(f"Failed to resend verification email to {email_lower} (SMTP not configured)")
            return {"message": "Verification email could not be sent. Please contact support."}
        
    except Exception as e:
        logger.error(f"Resend verification error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resend verification email"
        )


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Send password reset email to user.
    
    Args:
        request: Request body containing email
        
    Returns:
        Success message (always returns success for security - doesn't reveal if email exists)
    """
    try:
        email_lower = request.email.lower().strip()
        
        # Find user by email
        user = db.query(User).filter(User.email.ilike(email_lower)).first()
        
        # Security: Always return success message, don't reveal if user exists
        # This prevents email enumeration attacks
        if not user:
            logger.info(f"Password reset requested for non-existent email: {email_lower}")
            return {
                "message": "If an account with that email exists, a password reset link has been sent."
            }
        
        # Generate reset token
        email_service = get_email_service()
        reset_token = email_service.generate_verification_token()
        token_expires = datetime.now(timezone.utc) + timedelta(hours=1)  # 1 hour expiry
        
        # Update user with reset token
        user.reset_token = reset_token
        user.reset_token_expires = token_expires
        db.commit()
        
        # Send password reset email
        email_sent = email_service.send_password_reset_email(
            email=email_lower,
            name=user.name,
            token=reset_token
        )
        
        if email_sent:
            logger.info(f"Password reset email sent to {email_lower}")
        else:
            logger.warning(f"Password reset email NOT sent to {email_lower} (SMTP not configured)")
            logger.info(f"Password reset token for {email_lower}: {reset_token}")
            logger.info(f"Reset URL: {email_service.frontend_url}/reset-password?token={reset_token}")
        
        # Always return success message (security best practice)
        return {
            "message": "If an account with that email exists, a password reset link has been sent."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        db.rollback()
        # Still return success to prevent email enumeration
        return {
            "message": "If an account with that email exists, a password reset link has been sent."
        }


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset user password with reset token.
    
    Args:
        request: Request body containing token and new password
        
    Returns:
        Success message
    """
    try:
        token = request.token
        new_password = request.new_password
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token is required"
            )
        
        # URL decode the token in case it was URL-encoded
        from urllib.parse import unquote
        token = unquote(token.strip())
        
        logger.info(f"Password reset attempt with token: {token[:20]}... (length: {len(token)})")
        
        # Find user by reset token - try both the decoded token and the original
        user = db.query(User).filter(User.reset_token == token).first()
        
        # If not found, try without URL decoding (in case it wasn't encoded)
        if not user:
            original_token = request.token.strip()
            if original_token != token:
                logger.info(f"Trying original token (not URL-decoded): {original_token[:20]}...")
                user = db.query(User).filter(User.reset_token == original_token).first()
        
        if not user:
            logger.warning(f"Password reset failed - token not found: {token[:20]}...")
            # Check if any reset tokens exist (for debugging)
            token_count = db.query(User).filter(User.reset_token.isnot(None)).count()
            logger.info(f"Total users with reset tokens in database: {token_count}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Check if token is expired
        if user.reset_token_expires:
            # Ensure both datetimes are timezone-aware for comparison
            expires = user.reset_token_expires
            if expires.tzinfo is None:
                # If database returned naive datetime, assume UTC
                expires = expires.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            if expires < now:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Reset token has expired. Please request a new one."
                )
        
        # Validate password length
        password_bytes = len(new_password.encode('utf-8'))
        if password_bytes > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password is too long ({password_bytes} bytes). Maximum is 72 bytes."
            )
        
        # Update password
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        
        logger.info(f"Password reset successful for user: {user.email}")
        return {"message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reset password error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )


