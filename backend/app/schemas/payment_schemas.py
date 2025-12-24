"""
Payment and subscription schemas for Stripe integration.
"""
from pydantic import BaseModel, Field
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
    """Request to create a Stripe checkout session."""
    plan: SubscriptionPlan = Field(..., description="Subscription plan to purchase")
    success_url: Optional[str] = Field(None, description="URL to redirect after successful payment")
    cancel_url: Optional[str] = Field(None, description="URL to redirect after canceled payment")


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

