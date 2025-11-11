"""
Stripe service for handling payment processing.
"""

import stripe
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from app.models.database import User
from app.utils.config import settings


class StripeService:
    """Stripe service for managing payments and checkout sessions."""

    def __init__(self):
        """Initialize Stripe service with API key from settings."""
        if settings.STRIPE_SECRET_KEY:
            stripe.api_key = settings.STRIPE_SECRET_KEY
        else:
            raise ValueError("STRIPE_SECRET_KEY is not configured")

    def get_or_create_customer(
        self,
        db: Session,
        user: User
    ) -> str:
        """
        Get or create a Stripe customer for the user.

        Args:
            db: Database session
            user: User object

        Returns:
            Stripe customer ID

        Raises:
            stripe.error.StripeError: If Stripe API call fails
        """
        try:
            # Check if user has any payments with a Stripe customer ID
            from app.models.database import Payment

            existing_payment = db.query(Payment).filter(
                Payment.user_id == user.id,
                Payment.stripe_customer_id.isnot(None)
            ).first()

            if existing_payment and existing_payment.stripe_customer_id:
                # Verify the customer still exists in Stripe
                try:
                    stripe.Customer.retrieve(existing_payment.stripe_customer_id)
                    return existing_payment.stripe_customer_id
                except stripe.error.InvalidRequestError:
                    # Customer doesn't exist in Stripe, create a new one
                    pass

            # Create new Stripe customer
            customer = stripe.Customer.create(
                email=user.email,
                name=user.full_name,
                metadata={
                    "user_id": str(user.id),
                    "username": user.username
                }
            )

            return customer.id

        except stripe.error.StripeError as e:
            print(f"Stripe API error in get_or_create_customer: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in get_or_create_customer: {e}")
            raise

    def create_checkout_session(
        self,
        customer_id: str,
        amount: int,
        currency: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout session.

        Args:
            customer_id: Stripe customer ID
            amount: Amount in cents (e.g., 1000 = $10.00)
            currency: Currency code (e.g., "usd")
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect if payment is cancelled
            metadata: Optional metadata to attach to the session

        Returns:
            Dictionary containing session_id and checkout_url

        Raises:
            stripe.error.StripeError: If Stripe API call fails
        """
        try:
            # Validate amount
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")

            # Create line items for the checkout session
            line_items = [
                {
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
                        "product_data": {
                            "name": "AI Chatbot Credits",
                            "description": f"Purchase credits for AI Chatbot service"
                        }
                    },
                    "quantity": 1
                }
            ]

            # Prepare session parameters
            session_params = {
                "customer": customer_id,
                "line_items": line_items,
                "mode": "payment",
                "success_url": success_url,
                "cancel_url": cancel_url,
                "payment_method_types": ["card"],
            }

            # Add metadata if provided
            if metadata:
                session_params["metadata"] = metadata

            # Create checkout session
            session = stripe.checkout.Session.create(**session_params)

            return {
                "session_id": session.id,
                "checkout_url": session.url
            }

        except stripe.error.InvalidRequestError as e:
            print(f"Invalid request error in create_checkout_session: {e}")
            raise
        except stripe.error.StripeError as e:
            print(f"Stripe API error in create_checkout_session: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in create_checkout_session: {e}")
            raise

    def retrieve_session(self, session_id: str) -> Dict[str, Any]:
        """
        Retrieve a Stripe Checkout session by ID.

        Args:
            session_id: Stripe checkout session ID

        Returns:
            Dictionary containing session details

        Raises:
            stripe.error.StripeError: If Stripe API call fails
        """
        try:
            # Retrieve the session
            session = stripe.checkout.Session.retrieve(session_id)

            # Return relevant session details
            return {
                "id": session.id,
                "customer": session.customer,
                "payment_status": session.payment_status,
                "payment_intent": session.payment_intent,
                "amount_total": session.amount_total,
                "currency": session.currency,
                "metadata": session.metadata,
                "status": session.status
            }

        except stripe.error.InvalidRequestError as e:
            print(f"Invalid request error in retrieve_session: {e}")
            raise
        except stripe.error.StripeError as e:
            print(f"Stripe API error in retrieve_session: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in retrieve_session: {e}")
            raise


# Global instance
stripe_service = StripeService()
