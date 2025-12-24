"""
Stripe payment and subscription routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Optional
import stripe
from datetime import datetime, timezone, timedelta

from app.core.database import get_db
from app.core.config import settings
from app.core.logging import logger
from app.models.models import User, Payment
from app.schemas.payment_schemas import (
    CreateCheckoutRequest,
    CheckoutSessionResponse,
    SubscriptionResponse,
    PaymentResponse,
    SubscriptionPlan,
    SubscriptionStatus,
    PaymentStatus,
)
from app.api.routes.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Plan configuration
PLAN_CONFIG = {
    "starter": {
        "price_id": settings.STRIPE_PRICE_STARTER,
        "amount": 9.00,
        "name": "Starter",
    },
    "professional": {
        "price_id": settings.STRIPE_PRICE_PROFESSIONAL,
        "amount": 29.00,
        "name": "Professional",
        "trial_days": 14,
    },
}


@router.post("/create-checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CreateCheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a Stripe Checkout session for subscription.
    
    Requires: User authentication
    """
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    try:
        plan_config = PLAN_CONFIG.get(request.plan.value)
        if not plan_config:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid plan: {request.plan.value}"
            )
        
        # Get or create Stripe customer
        customer_id = current_user.stripe_customer_id
        if not customer_id:
            customer = stripe.Customer.create(
                email=current_user.email,
                name=current_user.name,
                metadata={"user_id": str(current_user.id)},
            )
            customer_id = customer.id
            current_user.stripe_customer_id = customer_id
            db.commit()
        
        # Build checkout session parameters
        checkout_params = {
            "customer": customer_id,
            "payment_method_types": ["card"],
            "mode": "subscription",
            "line_items": [
                {
                    "price": plan_config["price_id"],
                    "quantity": 1,
                }
            ],
            "success_url": request.success_url or f"{settings.cors_origins_list[0]}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url": request.cancel_url or f"{settings.cors_origins_list[0]}/pricing",
            "metadata": {
                "user_id": str(current_user.id),
                "plan": request.plan.value,
            },
        }
        
        # Add trial period for Professional plan
        if request.plan.value == "professional" and "trial_days" in plan_config:
            checkout_params["subscription_data"] = {
                "trial_period_days": plan_config["trial_days"],
            }
        
        # Create checkout session
        session = stripe.checkout.Session.create(**checkout_params)
        
        logger.info(f"Created checkout session {session.id} for user {current_user.id}, plan {request.plan.value}")
        
        return CheckoutSessionResponse(
            checkout_url=session.url,
            session_id=session.id,
        )
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating checkout: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment processing error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session"
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: str = Header(None),
):
    """
    Handle Stripe webhook events.
    
    This endpoint receives events from Stripe about payment status changes.
    """
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret not configured"
        )
    
    payload = await request.body()
    
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    event_type = event["type"]
    event_data = event["data"]["object"]
    
    logger.info(f"Received Stripe webhook: {event_type}")
    
    try:
        if event_type == "checkout.session.completed":
            # Payment successful, subscription created
            session = event_data
            user_id = int(session["metadata"]["user_id"])
            plan = session["metadata"]["plan"]
            
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                subscription_id = session.get("subscription")
                if subscription_id:
                    # Get subscription details from Stripe
                    subscription = stripe.Subscription.retrieve(subscription_id)
                    
                    user.stripe_subscription_id = subscription_id
                    user.subscription_plan = plan
                    user.subscription_status = subscription.status
                    user.subscription_start_date = datetime.fromtimestamp(
                        subscription.current_period_start, tz=timezone.utc
                    )
                    user.subscription_end_date = datetime.fromtimestamp(
                        subscription.current_period_end, tz=timezone.utc
                    )
                    if subscription.trial_end:
                        user.trial_end_date = datetime.fromtimestamp(
                            subscription.trial_end, tz=timezone.utc
                        )
                    
                    db.commit()
                    logger.info(f"Updated subscription for user {user_id}: {plan}")
        
        elif event_type == "customer.subscription.updated":
            # Subscription updated (e.g., plan change, renewal)
            subscription = event_data
            customer_id = subscription["customer"]
            
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.subscription_status = subscription["status"]
                user.subscription_end_date = datetime.fromtimestamp(
                    subscription["current_period_end"], tz=timezone.utc
                )
                db.commit()
                logger.info(f"Updated subscription status for user {user.id}")
        
        elif event_type == "customer.subscription.deleted":
            # Subscription canceled
            subscription = event_data
            customer_id = subscription["customer"]
            
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.subscription_status = "canceled"
                user.subscription_end_date = datetime.fromtimestamp(
                    subscription["current_period_end"], tz=timezone.utc
                )
                db.commit()
                logger.info(f"Canceled subscription for user {user.id}")
        
        elif event_type == "invoice.payment_succeeded":
            # Payment succeeded - record payment
            invoice = event_data
            customer_id = invoice["customer"]
            
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                payment = Payment(
                    user_id=user.id,
                    stripe_invoice_id=invoice["id"],
                    amount=invoice["amount_paid"] / 100,  # Convert from cents
                    currency=invoice["currency"],
                    status="succeeded",
                    subscription_plan=user.subscription_plan,
                    billing_period_start=datetime.fromtimestamp(
                        invoice["period_start"], tz=timezone.utc
                    ) if invoice.get("period_start") else None,
                    billing_period_end=datetime.fromtimestamp(
                        invoice["period_end"], tz=timezone.utc
                    ) if invoice.get("period_end") else None,
                )
                db.add(payment)
                db.commit()
                logger.info(f"Recorded payment for user {user.id}")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing webhook {event_type}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing webhook: {str(e)}"
        )


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's subscription information.
    
    Requires: User authentication
    """
    return SubscriptionResponse(
        plan=current_user.subscription_plan,
        status=current_user.subscription_status,
        current_period_start=current_user.subscription_start_date,
        current_period_end=current_user.subscription_end_date,
        trial_end=current_user.trial_end_date,
        cancel_at_period_end=False,  # Can be enhanced to check Stripe
        is_active=current_user.subscription_status == "active",
    )


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Cancel user's subscription.
    
    Requires: User authentication
    """
    if not current_user.stripe_subscription_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription found"
        )
    
    try:
        # Cancel subscription at period end
        subscription = stripe.Subscription.modify(
            current_user.stripe_subscription_id,
            cancel_at_period_end=True,
        )
        
        current_user.subscription_status = "canceled"
        db.commit()
        
        logger.info(f"Canceled subscription for user {current_user.id}")
        
        return {
            "message": "Subscription will be canceled at the end of the billing period",
            "cancel_at": datetime.fromtimestamp(
                subscription.current_period_end, tz=timezone.utc
            ).isoformat(),
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error canceling subscription: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to cancel subscription: {str(e)}"
        )


@router.get("/history", response_model=list[PaymentResponse])
async def get_payment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get user's payment history.
    
    Requires: User authentication
    """
    payments = db.query(Payment).filter(Payment.user_id == current_user.id).order_by(
        Payment.created_at.desc()
    ).limit(50).all()
    
    return payments

