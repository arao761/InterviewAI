"""
Admin routes for manual user management and system health checks.
These endpoints should be protected in production with proper authentication.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.core.logging import logger
from app.services.email_service import get_email_service
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


class ManualVerifyRequest(BaseModel):
    """Request to manually verify a user."""
    email: EmailStr


class UserListResponse(BaseModel):
    """Response for listing users."""
    id: int
    email: str
    name: str
    email_verified: bool
    created_at: datetime
    verification_token: Optional[str] = None


class SMTPHealthResponse(BaseModel):
    """Response for SMTP health check."""
    configured: bool
    can_connect: bool
    error: Optional[str] = None


@router.post("/verify-user", status_code=status.HTTP_200_OK)
async def manually_verify_user(
    request: ManualVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Manually verify a user's email address (admin only).
    
    Use this when email verification fails or SMTP is not configured.
    """
    try:
        email_lower = request.email.lower().strip()
        user = db.query(User).filter(User.email.ilike(email_lower)).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found: {email_lower}"
            )
        
        if user.email_verified:
            return {
                "message": f"User {user.email} is already verified",
                "email_verified": True
            }
        
        # Manually verify the user
        user.email_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        db.commit()
        
        logger.info(f"✅ Admin manually verified user: {user.email}")
        return {
            "message": f"User {user.email} has been manually verified",
            "email_verified": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Manual verification error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify user: {str(e)}"
        )


@router.get("/unverified-users", response_model=List[UserListResponse])
async def list_unverified_users(db: Session = Depends(get_db)):
    """
    List all unverified users (admin only).
    """
    try:
        users = db.query(User).filter(User.email_verified == False).all()
        
        return [
            UserListResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                email_verified=user.email_verified,
                created_at=user.created_at,
                verification_token=user.verification_token[:30] + "..." if user.verification_token else None
            )
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error listing unverified users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list unverified users"
        )


@router.get("/smtp-health", response_model=SMTPHealthResponse)
async def check_smtp_health():
    """
    Check SMTP configuration and connectivity (admin only).
    """
    try:
        email_service = get_email_service()
        
        # Check if SMTP is configured
        if not email_service.smtp_user or not email_service.smtp_password:
            return SMTPHealthResponse(
                configured=False,
                can_connect=False,
                error="SMTP_USER or SMTP_PASSWORD not configured"
            )
        
        # Try to connect to SMTP server
        try:
            import smtplib
            with smtplib.SMTP(email_service.smtp_host, email_service.smtp_port, timeout=5) as server:
                server.starttls()
                server.login(email_service.smtp_user, email_service.smtp_password)
            
            return SMTPHealthResponse(
                configured=True,
                can_connect=True,
                error=None
            )
        except smtplib.SMTPAuthenticationError as e:
            return SMTPHealthResponse(
                configured=True,
                can_connect=False,
                error=f"SMTP authentication failed: {str(e)}"
            )
        except Exception as e:
            return SMTPHealthResponse(
                configured=True,
                can_connect=False,
                error=f"SMTP connection error: {str(e)}"
            )
            
    except Exception as e:
        logger.error(f"SMTP health check error: {e}")
        return SMTPHealthResponse(
            configured=False,
            can_connect=False,
            error=f"Health check failed: {str(e)}"
        )


@router.get("/user/{email}")
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Get user information by email (admin only).
    """
    try:
        email_lower = email.lower().strip()
        user = db.query(User).filter(User.email.ilike(email_lower)).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found: {email_lower}"
            )
        
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "email_verified": user.email_verified,
            "created_at": user.created_at,
            "has_verification_token": user.verification_token is not None,
            "token_expires": user.verification_token_expires
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )

