"""
Payment router for handling Stripe checkout sessions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.models.database import User
from app.models.schemas import CheckoutSessionCreate, CheckoutSessionResponse
from app.services.auth import get_current_active_user
from app.services.database import get_db
from app.services.stripe_service import stripe_service

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
