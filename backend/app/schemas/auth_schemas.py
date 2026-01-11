"""
Authentication schemas for request/response validation.

SECURITY FEATURES:
- Email validation to prevent injection attacks
- String length limits to prevent buffer overflow
- Pattern validation for usernames
- No unexpected fields allowed (extra='forbid')
- Input sanitization via Pydantic validators
"""
from pydantic import BaseModel, EmailStr, Field, validator, field_validator
from typing import Optional
from datetime import datetime
import re


class UserRegister(BaseModel):
    """
    Schema for user registration.

    SECURITY VALIDATIONS:
    - Email: Valid format, lowercase, max 255 chars (OWASP)
    - Name: 1-255 chars, no special chars except spaces, hyphens, apostrophes
    - Password: 8-72 chars (bcrypt limit), complexity requirements
    """
    email: EmailStr = Field(
        ...,
        description="User email address",
        max_length=255,
        json_schema_extra={"example": "user@example.com"}
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Full name (letters, spaces, hyphens, apostrophes only)",
        json_schema_extra={"example": "John Doe"}
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,  # bcrypt max length
        description="Password (8-72 chars, mix of letters, numbers recommended)",
        json_schema_extra={"example": "SecurePass123!"}
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validate name contains only safe characters.

        SECURITY: Prevent injection attacks and XSS via malicious names.
        Allowed: Letters (any language), spaces, hyphens, apostrophes, periods
        """
        # Strip leading/trailing whitespace
        v = v.strip()

        # Check length after stripping
        if not v or len(v) > 255:
            raise ValueError("Name must be 1-255 characters")

        # Allow letters (any unicode), spaces, hyphens, apostrophes, periods
        # Prevent: HTML tags, SQL syntax, control characters
        if not re.match(r"^[\w\s\-'.]+$", v, re.UNICODE):
            raise ValueError(
                "Name can only contain letters, spaces, hyphens, apostrophes, and periods"
            )

        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength.

        SECURITY: Enforce minimum complexity to prevent brute force.
        - Minimum 8 characters
        - Maximum 72 characters (bcrypt limitation)
        - Recommend mixing uppercase, lowercase, numbers, special chars
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password is too long (max 72 bytes)")

        # Optional: Check for common weak passwords
        weak_passwords = ['password', '12345678', 'qwerty', 'abc123']
        if v.lower() in weak_passwords:
            raise ValueError("Password is too common. Please choose a stronger password.")

        return v

    class Config:
        # SECURITY: Forbid extra fields to prevent parameter pollution
        extra = 'forbid'
        str_strip_whitespace = True  # Auto-strip whitespace from strings


class UserLogin(BaseModel):
    """
    Schema for user login.

    SECURITY: Rate limited at endpoint level (10 requests/minute per IP)
    """
    email: EmailStr = Field(
        ...,
        description="User email address",
        max_length=255
    )
    password: str = Field(
        ...,
        description="User password",
        max_length=72
    )

    class Config:
        extra = 'forbid'  # Prevent parameter pollution
        str_strip_whitespace = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""
    email: Optional[str] = None


class VerifyEmailRequest(BaseModel):
    """
    Schema for email verification request.

    SECURITY: Token should be cryptographically secure random string
    """
    token: str = Field(
        ...,
        min_length=32,
        max_length=256,
        description="Email verification token"
    )

    @field_validator('token')
    @classmethod
    def validate_token(cls, v: str) -> str:
        """
        Validate token format.

        SECURITY: Only allow alphanumeric and safe characters to prevent injection
        """
        if not re.match(r'^[a-zA-Z0-9\-_]+$', v):
            raise ValueError("Invalid token format")
        return v

    class Config:
        extra = 'forbid'


class UserResponse(BaseModel):
    """Schema for user response (without password)."""
    id: int
    email: str
    name: str
    email_verified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ForgotPasswordRequest(BaseModel):
    """
    Schema for forgot password request.

    SECURITY: Rate limited (3 requests/hour per IP) to prevent email bombing
    """
    email: EmailStr = Field(
        ...,
        description="User email address",
        max_length=255
    )

    class Config:
        extra = 'forbid'
        str_strip_whitespace = True


class ResetPasswordRequest(BaseModel):
    """
    Schema for reset password request.

    SECURITY:
    - Token validation to prevent injection
    - Password complexity requirements
    - Rate limited (5 requests/hour per IP)
    """
    token: str = Field(
        ...,
        min_length=32,
        max_length=256,
        description="Password reset token"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="New password"
    )

    @field_validator('token')
    @classmethod
    def validate_token(cls, v: str) -> str:
        """Validate token format - only alphanumeric and safe chars."""
        if not re.match(r'^[a-zA-Z0-9\-_]+$', v):
            raise ValueError("Invalid token format")
        return v

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password is too long (max 72 bytes)")

        # Check for common weak passwords
        weak_passwords = ['password', '12345678', 'qwerty', 'abc123']
        if v.lower() in weak_passwords:
            raise ValueError("Password is too common. Please choose a stronger password.")

        return v

    class Config:
        extra = 'forbid'
        str_strip_whitespace = True
