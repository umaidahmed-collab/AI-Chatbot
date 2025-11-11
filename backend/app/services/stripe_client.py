"""
Stripe client initialization and configuration.
"""

import logging
from typing import Optional
import stripe
from pydantic import BaseModel, Field

from app.utils.config import settings

logger = logging.getLogger(__name__)


class StripeConfig(BaseModel):
    """Stripe configuration settings."""

    secret_key: str = Field(default="", description="Stripe secret API key")
    publishable_key: str = Field(default="", description="Stripe publishable key")
    webhook_secret: str = Field(default="", description="Stripe webhook secret")
    api_version: str = Field(default="2023-10-16", description="Stripe API version")

    class Config:
        frozen = True  # Make immutable

    @property
    def is_configured(self) -> bool:
        """Check if Stripe is properly configured with minimum required settings."""
        return bool(self.secret_key and self.publishable_key)

    def validate_configuration(self) -> None:
        """
        Validate Stripe configuration.

        Raises:
            ValueError: If required Stripe keys are missing.
        """
        if not self.secret_key:
            raise ValueError(
                "STRIPE_SECRET_KEY is not configured. "
                "Please set it in your environment or .env file."
            )
        if not self.publishable_key:
            raise ValueError(
                "STRIPE_PUBLISHABLE_KEY is not configured. "
                "Please set it in your environment or .env file."
            )


# Initialize Stripe configuration from settings
stripe_config = StripeConfig(
    secret_key=settings.STRIPE_SECRET_KEY,
    publishable_key=settings.STRIPE_PUBLISHABLE_KEY,
    webhook_secret=settings.STRIPE_WEBHOOK_SECRET,
    api_version="2023-10-16"
)


def get_stripe_client() -> Optional[stripe]:
    """
    Get configured Stripe client instance.

    Returns:
        stripe module configured with API key, or None if not configured.

    Raises:
        ValueError: If Stripe keys are missing when called in production mode.

    Example:
        ```python
        stripe_client = get_stripe_client()
        if stripe_client:
            customer = stripe_client.Customer.create(email="user@example.com")
        ```
    """
    if not stripe_config.is_configured:
        # In development, log warning and return None
        if settings.ENVIRONMENT == "development":
            logger.warning(
                "Stripe is not configured. Stripe features will be disabled. "
                "Set STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY to enable."
            )
            return None
        else:
            # In production, raise error
            stripe_config.validate_configuration()

    try:
        # Configure Stripe with API key and version
        stripe.api_key = stripe_config.secret_key
        stripe.api_version = stripe_config.api_version

        logger.info(
            f"Stripe client initialized successfully with API version {stripe_config.api_version}"
        )
        return stripe

    except Exception as e:
        logger.error(f"Failed to initialize Stripe client: {str(e)}")
        if settings.ENVIRONMENT == "production":
            raise
        return None


def verify_stripe_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify Stripe webhook signature.

    Args:
        payload: Raw request body bytes
        signature: Stripe-Signature header value

    Returns:
        True if signature is valid, False otherwise.
    """
    if not stripe_config.webhook_secret:
        logger.warning("Stripe webhook secret not configured. Skipping signature verification.")
        return False

    try:
        stripe.Webhook.construct_event(
            payload, signature, stripe_config.webhook_secret
        )
        return True
    except ValueError as e:
        logger.error(f"Invalid webhook payload: {str(e)}")
        return False
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid webhook signature: {str(e)}")
        return False


# Initialize Stripe client on module import for convenience
stripe_client = get_stripe_client()
