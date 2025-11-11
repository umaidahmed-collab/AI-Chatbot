"""
Payment router for handling Stripe checkout sessions.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import stripe

from app.models.database import User
from app.models.schemas import CheckoutSessionCreate, CheckoutSessionResponse
from app.services.auth import get_current_active_user
from app.services.database import get_db
from app.services.stripe_service import stripe_service
from app.utils.config import settings

router = APIRouter()


@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    checkout_data: CheckoutSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a Stripe Checkout session for the current user.

    Args:
        checkout_data: Checkout session details including amount, currency, and redirect URLs
        current_user: Authenticated user
        db: Database session

    Returns:
        CheckoutSessionResponse with session_id and checkout_url

    Raises:
        HTTPException: If session creation fails
    """
    try:
        # Get or create Stripe customer for the user
        customer_id = stripe_service.get_or_create_customer(db, current_user)

        # Prepare metadata for the session
        metadata = {
            "user_id": str(current_user.id),
            "username": current_user.username
        }

        # Create checkout session
        session_data = stripe_service.create_checkout_session(
            customer_id=customer_id,
            amount=checkout_data.amount,
            currency=checkout_data.currency,
            success_url=checkout_data.success_url,
            cancel_url=checkout_data.cancel_url,
            metadata=metadata
        )

        return CheckoutSessionResponse(
            session_id=session_data["session_id"],
            checkout_url=session_data["checkout_url"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session"
        )


@router.get("/session/{session_id}")
async def get_session_status(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Retrieve the status of a Stripe Checkout session.

    Args:
        session_id: Stripe checkout session ID
        current_user: Authenticated user

    Returns:
        Dictionary containing session details and payment status

    Raises:
        HTTPException: If session retrieval fails
    """
    try:
        # Retrieve session details from Stripe
        session_data = stripe_service.retrieve_session(session_id)

        return {
            "session_id": session_data["id"],
            "payment_status": session_data["payment_status"],
            "status": session_data["status"],
            "amount_total": session_data["amount_total"],
            "currency": session_data["currency"]
        }

    except Exception as e:
        print(f"Error retrieving session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session status"
        )


@router.get("/success")
async def payment_success(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Handle successful payment redirect.

    Args:
        session_id: Stripe checkout session ID from query parameter
        current_user: Authenticated user

    Returns:
        Dictionary with success message and session details

    Raises:
        HTTPException: If session retrieval fails
    """
    try:
        # Retrieve session to verify payment status
        session_data = stripe_service.retrieve_session(session_id)

        return {
            "success": True,
            "message": "Payment completed successfully",
            "session_id": session_data["id"],
            "payment_status": session_data["payment_status"],
            "amount_total": session_data["amount_total"],
            "currency": session_data["currency"]
        }

    except Exception as e:
        print(f"Error processing payment success: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process payment success"
        )


@router.get("/cancel")
async def payment_cancel(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Handle cancelled payment redirect.

    Args:
        session_id: Stripe checkout session ID from query parameter
        current_user: Authenticated user

    Returns:
        Dictionary with cancellation message and session details
    """
    return {
        "success": False,
        "message": "Payment was cancelled",
        "session_id": session_id
    }


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: Optional[str] = Header(None, alias="stripe-signature")
) -> Dict[str, Any]:
    """
    Handle Stripe webhook events.

    This endpoint receives webhook events from Stripe, verifies the signature,
    and processes the events accordingly. It handles:
    - checkout.session.completed: Creates a payment record in the database
    - checkout.session.expired: Updates payment status to expired

    Args:
        request: FastAPI request object containing the raw webhook payload
        db: Database session
        stripe_signature: Stripe signature header for webhook verification

    Returns:
        Dictionary with success status

    Raises:
        HTTPException: If webhook verification fails or processing encounters errors
    """
    # Get raw body for signature verification
    try:
        payload = await request.body()
    except Exception as e:
        print(f"Error reading request body: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request body"
        )

    # Verify webhook signature
    if not stripe_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )

    if not settings.STRIPE_WEBHOOK_SECRET:
        print("Warning: STRIPE_WEBHOOK_SECRET not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret not configured"
        )

    try:
        event = stripe_service.construct_webhook_event(
            payload=payload,
            signature=stripe_signature,
            webhook_secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as e:
        print(f"Webhook signature verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )
    except Exception as e:
        print(f"Error constructing webhook event: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook payload"
        )

    # Handle the event
    event_type = event["type"]
    event_data = event["data"]["object"]

    try:
        if event_type == "checkout.session.completed":
            # Handle successful checkout session
            print(f"Processing checkout.session.completed for session {event_data['id']}")

            # Retrieve full session details from Stripe
            session_data = stripe_service.retrieve_session(event_data["id"])

            # Create payment record in database
            payment = stripe_service.create_payment_record(db, session_data)

            if payment:
                print(f"Payment record created: {payment.id}")
            else:
                print("Failed to create payment record")

        elif event_type == "checkout.session.expired":
            # Handle expired checkout session
            print(f"Processing checkout.session.expired for session {event_data['id']}")

            # Update payment status to expired
            updated = stripe_service.update_payment_status(
                db,
                checkout_session_id=event_data["id"],
                status="expired"
            )

            if updated:
                print(f"Payment status updated to expired for session {event_data['id']}")
            else:
                print(f"No existing payment found for expired session {event_data['id']}")

        else:
            # Log unhandled event types
            print(f"Unhandled webhook event type: {event_type}")

    except Exception as e:
        print(f"Error processing webhook event {event_type}: {e}")
        # Return 200 anyway to acknowledge receipt
        # Stripe will retry if we return an error

    # Always return 200 to acknowledge receipt
    return {"success": True}
