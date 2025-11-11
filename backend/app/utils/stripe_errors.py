"""
Stripe error handling utilities.

This module provides custom exception classes and error handling functions
for Stripe API interactions.
"""
from typing import Optional, Dict, Any
import stripe
from stripe.error import (
    CardError,
    InvalidRequestError,
    AuthenticationError,
    APIConnectionError,
    RateLimitError,
    StripeError as StripeAPIError,
)


class StripeError(Exception):
    """
    Custom exception class for Stripe-related errors.

    Attributes:
        message: Human-readable error message
        error_code: Stripe error code (if available)
        error_type: Type of Stripe error
        status_code: HTTP status code (if available)
        original_error: Original Stripe exception
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        error_type: Optional[str] = None,
        status_code: Optional[int] = None,
        original_error: Optional[Exception] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.error_type = error_type
        self.status_code = status_code
        self.original_error = original_error
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary format for API responses."""
        return {
            "error": {
                "message": self.message,
                "code": self.error_code,
                "type": self.error_type,
                "status_code": self.status_code,
            }
        }


def handle_stripe_error(error: Exception) -> StripeError:
    """
    Convert Stripe API errors to application-specific StripeError exceptions.

    This function maps different Stripe error types to a unified StripeError
    exception with appropriate error messages and metadata.

    Args:
        error: The original Stripe exception

    Returns:
        StripeError: A custom exception with normalized error information

    Example:
        try:
            stripe.PaymentIntent.create(...)
        except Exception as e:
            raise handle_stripe_error(e)
    """

    # CardError - card was declined or invalid card details
    if isinstance(error, CardError):
        return StripeError(
            message=error.user_message or "The card was declined.",
            error_code=error.code,
            error_type="card_error",
            status_code=error.http_status,
            original_error=error,
        )

    # InvalidRequestError - invalid parameters or request
    elif isinstance(error, InvalidRequestError):
        return StripeError(
            message=f"Invalid request to Stripe API: {str(error)}",
            error_code=error.code,
            error_type="invalid_request_error",
            status_code=error.http_status,
            original_error=error,
        )

    # AuthenticationError - authentication with Stripe's API failed
    elif isinstance(error, AuthenticationError):
        return StripeError(
            message="Authentication with payment provider failed. Please contact support.",
            error_code=error.code,
            error_type="authentication_error",
            status_code=error.http_status,
            original_error=error,
        )

    # APIConnectionError - network communication failed
    elif isinstance(error, APIConnectionError):
        return StripeError(
            message="Unable to connect to payment provider. Please try again later.",
            error_code=None,
            error_type="api_connection_error",
            status_code=None,
            original_error=error,
        )

    # RateLimitError - too many requests hit the API too quickly
    elif isinstance(error, RateLimitError):
        return StripeError(
            message="Too many requests. Please try again in a moment.",
            error_code=error.code,
            error_type="rate_limit_error",
            status_code=error.http_status,
            original_error=error,
        )

    # Generic StripeError - catch-all for other Stripe errors
    elif isinstance(error, StripeAPIError):
        return StripeError(
            message=f"Payment processing error: {str(error)}",
            error_code=getattr(error, "code", None),
            error_type="stripe_error",
            status_code=getattr(error, "http_status", None),
            original_error=error,
        )

    # Non-Stripe error - wrap in StripeError for consistent handling
    else:
        return StripeError(
            message=f"Unexpected error during payment processing: {str(error)}",
            error_code=None,
            error_type="unknown_error",
            status_code=None,
            original_error=error,
        )
