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
            
            # Safely extract metadata
            metadata = session.get("metadata", {})
            user_id = metadata.get("user_id")
            plan = metadata.get("plan")
            
            if not user_id or not plan:
                logger.error(f"Missing metadata in checkout.session.completed: {session}")
                return {"status": "error", "message": "Missing required metadata"}
            
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                logger.error(f"Invalid user_id in metadata: {user_id}")
                return {"status": "error", "message": "Invalid user_id"}
            
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"User not found for checkout session: {user_id}")
                return {"status": "error", "message": "User not found"}
            
            subscription_id = session.get("subscription")
            if subscription_id:
                try:
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
                except stripe.error.StripeError as e:
                    logger.error(f"Stripe error retrieving subscription: {e}")
                    db.rollback()
                    return {"status": "error", "message": f"Stripe error: {str(e)}"}
            else:
                logger.warning(f"No subscription ID in checkout session: {session.get('id')}")
        
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
            customer_id = invoice.get("customer")
            
            if not customer_id:
                logger.error(f"Missing customer ID in invoice: {invoice.get('id')}")
                return {"status": "error", "message": "Missing customer ID"}
            
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if not user:
                logger.warning(f"User not found for customer: {customer_id}")
                return {"status": "warning", "message": "User not found"}
            
            # Check if payment already exists to avoid duplicates
            existing_payment = db.query(Payment).filter(
                Payment.stripe_invoice_id == invoice["id"]
            ).first()
            
            if existing_payment:
                logger.info(f"Payment already recorded for invoice: {invoice['id']}")
                return {"status": "success", "message": "Payment already recorded"}
            
            try:
                amount_paid = invoice.get("amount_paid", 0) / 100  # Convert from cents
                payment = Payment(
                    user_id=user.id,
                    stripe_invoice_id=invoice["id"],
                    amount=amount_paid,
                    currency=invoice.get("currency", "usd"),
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
                logger.info(f"Recorded payment for user {user.id}: ${amount_paid}")
            except Exception as e:
                logger.error(f"Error recording payment: {e}")
                db.rollback()
                return {"status": "error", "message": f"Error recording payment: {str(e)}"}
        
        elif event_type == "invoice.payment_failed":
            # Payment failed - update subscription status
            invoice = event_data
            customer_id = invoice.get("customer")
            
            if customer_id:
                user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
                if user:
                    user.subscription_status = "past_due"
                    db.commit()
                    logger.warning(f"Payment failed for user {user.id}, subscription set to past_due")
        
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
    db: Session = Depends(get_db),
):
    """
    Get current user's subscription information.
    
    Requires: User authentication
    
    If user has a Stripe subscription, fetches latest status from Stripe
    to ensure data is up-to-date.
    """
    # If user has a Stripe subscription ID, fetch latest status from Stripe
    cancel_at_period_end = False
    if current_user.stripe_subscription_id and settings.STRIPE_SECRET_KEY:
        try:
            subscription = stripe.Subscription.retrieve(current_user.stripe_subscription_id)
            cancel_at_period_end = subscription.cancel_at_period_end
            
            # Update local database if status changed
            if subscription.status != current_user.subscription_status:
                current_user.subscription_status = subscription.status
                db.commit()
                logger.info(f"Updated subscription status for user {current_user.id}: {subscription.status}")
        except stripe.error.StripeError as e:
            logger.warning(f"Could not fetch subscription from Stripe: {e}")
            # Continue with database values
    
    return SubscriptionResponse(
        plan=current_user.subscription_plan,
        status=current_user.subscription_status,
        current_period_start=current_user.subscription_start_date,
        current_period_end=current_user.subscription_end_date,
        trial_end=current_user.trial_end_date,
        cancel_at_period_end=cancel_at_period_end,
        is_active=current_user.subscription_status == "active" or current_user.subscription_status == "trialing",
    )


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Cancel user's subscription.
    
    Requires: User authentication
    
    Cancels the subscription at the end of the current billing period,
    allowing the user to continue using the service until then.
    """
    if not current_user.stripe_subscription_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription found"
        )
    
    # Check if already canceled
    if current_user.subscription_status == "canceled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscription is already canceled"
        )
    
    try:
        # Cancel subscription at period end (not immediately)
        subscription = stripe.Subscription.modify(
            current_user.stripe_subscription_id,
            cancel_at_period_end=True,
        )
        
        # Update status - subscription is still active until period end
        # The webhook will update it to "canceled" when period ends
        current_user.subscription_status = subscription.status
        db.commit()
        
        logger.info(f"Scheduled subscription cancellation for user {current_user.id}")
        
        cancel_at = datetime.fromtimestamp(
            subscription.current_period_end, tz=timezone.utc
        )
        
        return {
            "message": "Subscription will be canceled at the end of the billing period",
            "cancel_at": cancel_at.isoformat(),
            "cancel_at_formatted": cancel_at.strftime("%B %d, %Y"),
            "current_period_end": cancel_at.isoformat(),
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error canceling subscription: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to cancel subscription: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error canceling subscription: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while canceling subscription"
        )


@router.get("/checkout-session/{session_id}")
async def get_checkout_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    Get checkout session details from Stripe.
    
    Requires: User authentication
    """
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    try:
        # Retrieve session from Stripe
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['line_items', 'payment_intent', 'customer']
        )
        
        # Verify the session belongs to the current user
        if session.metadata and session.metadata.get('user_id'):
            if int(session.metadata['user_id']) != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This session does not belong to you"
                )
        
        # Return session details
        return {
            "id": session.id,
            "status": session.status,
            "payment_status": session.payment_status,
            "customer_details": {
                "email": session.customer_details.email if session.customer_details else None,
                "name": session.customer_details.name if session.customer_details else None,
            } if session.customer_details else None,
            "amount_total": session.amount_total / 100 if session.amount_total else None,
            "currency": session.currency,
            "created": session.created,
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error retrieving session: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve session: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error retrieving checkout session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve checkout session"
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

