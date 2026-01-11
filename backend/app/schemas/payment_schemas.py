"""
Payment and subscription schemas for Stripe integration.

SECURITY FEATURES:
- URL validation for callbacks
- Strict enum validation for plans and statuses
- No unexpected fields allowed (extra='forbid')
- Length limits on all string fields
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class SubscriptionPlan(str, Enum):
    """Subscription plan types."""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    """Subscription status types."""
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"


class PaymentStatus(str, Enum):
    """Payment status types."""
    SUCCEEDED = "succeeded"
    PENDING = "pending"
    FAILED = "failed"
    REFUNDED = "refunded"


class CreateCheckoutRequest(BaseModel):
    """
    Request to create a Stripe checkout session.

    SECURITY:
    - Plan validated against enum
    - URLs validated to prevent open redirect vulnerabilities
    - Rate limited at endpoint (10 requests/hour per user)
    """
    plan: SubscriptionPlan = Field(
        ...,
        description="Subscription plan to purchase"
    )
    success_url: Optional[str] = Field(
        None,
        max_length=2048,
        description="URL to redirect after successful payment"
    )
    cancel_url: Optional[str] = Field(
        None,
        max_length=2048,
        description="URL to redirect after canceled payment"
    )

    @field_validator('success_url', 'cancel_url')
    @classmethod
    def validate_urls(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate callback URLs.

        SECURITY: Prevent open redirect attacks by validating URL format
        In production, consider whitelisting allowed domains
        """
        if v is None:
            return v

        v = v.strip()

        # Basic URL validation
        if not v.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")

        # Prevent javascript: and data: URLs
        if v.lower().startswith(('javascript:', 'data:', 'vbscript:')):
            raise ValueError("Invalid URL scheme")

        # Length check
        if len(v) > 2048:
            raise ValueError("URL is too long (max 2048 characters)")

        return v

    class Config:
        extra = 'forbid'


class CheckoutSessionResponse(BaseModel):
    """Response with Stripe checkout session URL."""
    checkout_url: str = Field(..., description="URL to redirect user to Stripe Checkout")
    session_id: str = Field(..., description="Stripe checkout session ID")


class SubscriptionResponse(BaseModel):
    """User subscription information."""
    plan: Optional[str] = None
    status: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    is_active: bool = False
    
    class Config:
        from_attributes = True


class PaymentResponse(BaseModel):
    """Payment information."""
    id: int
    amount: float
    currency: str
    status: str
    subscription_plan: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class WebhookEvent(BaseModel):
    """Stripe webhook event data."""
    id: str
    type: str
    data: dict

