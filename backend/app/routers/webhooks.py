"""
Stripe webhooks router.

This endpoint receives and processes Stripe webhook events with signature verification
to ensure authenticity and prevent unauthorized access.
"""

import logging
from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services.stripe_service import StripeService, StripeWebhookError
from app.services.database import get_db

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Stripe webhook events.

    Security features:
    - Verifies webhook signature using Stripe-Signature header
    - Rejects requests with invalid signatures (400 Bad Request)
    - Processes raw request body to maintain signature integrity
    - Routes verified events to appropriate service handlers
    - Implements comprehensive error handling and logging

    Args:
        request: FastAPI request object (provides raw body and headers)
        db: Database session for transaction management

    Returns:
        Response with status 200 OK for successfully processed events
        Response with status 400 Bad Request for invalid signatures or malformed requests

    Raises:
        HTTPException: For signature verification failures or processing errors
    """
    # Extract Stripe signature header
    signature = request.headers.get("stripe-signature")

    if not signature:
        logger.error(
            "Webhook request missing Stripe-Signature header",
            extra={
                "remote_addr": request.client.host if request.client else "unknown"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )

    # Read raw request body (required for signature verification)
    try:
        payload = await request.body()
    except Exception as e:
        logger.error(f"Failed to read request body: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request body"
        )

    # Initialize Stripe service
    stripe_service = StripeService(db)

    try:
        # Verify webhook signature and construct event
        # This is the critical security step - prevents webhook spoofing
        event = stripe_service.verify_webhook_signature(payload, signature)

        # Log successful verification
        logger.info(
            f"Processing verified webhook event",
            extra={
                "event_id": event.get("id"),
                "event_type": event.get("type"),
                "remote_addr": request.client.host if request.client else "unknown"
            }
        )

        # Process the verified event (routes to appropriate handler)
        stripe_service.process_webhook_event(event)

        # Return 200 OK to acknowledge successful processing
        # This tells Stripe we've received and processed the webhook
        logger.info(
            f"Webhook processed successfully",
            extra={
                "event_id": event.get("id"),
                "event_type": event.get("type")
            }
        )

        return Response(
            content='{"status": "success"}',
            media_type="application/json",
            status_code=status.HTTP_200_OK
        )

    except ValueError as e:
        # Configuration error (webhook secret not set)
        logger.error(
            f"Webhook configuration error: {str(e)}",
            extra={
                "error_type": "configuration_error"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook configuration error"
        )

    except StripeWebhookError as e:
        # Signature verification failed or webhook processing error
        # Return 400 to signal to Stripe that we rejected this webhook
        logger.error(
            f"Webhook processing failed: {str(e)}",
            extra={
                "error_type": "webhook_error",
                "remote_addr": request.client.host if request.client else "unknown"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature or processing error"
        )

    except Exception as e:
        # Unexpected error
        logger.error(
            f"Unexpected error processing webhook: {str(e)}",
            extra={
                "error_type": "unexpected_error",
                "error": str(e)
            }
        )
        # Return 500 for unexpected errors
        # Stripe will retry the webhook automatically
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error processing webhook"
        )
