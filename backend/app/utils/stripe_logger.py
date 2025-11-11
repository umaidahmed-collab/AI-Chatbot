"""
Structured logging utilities for Stripe operations.

This module provides functions for logging Stripe events and errors with
sanitization to prevent sensitive data leakage.
"""

import logging
import re
from typing import Any, Dict, Optional
from datetime import datetime
import json

# Configure logger
logger = logging.getLogger("stripe_operations")


class StripeLogFormatter(logging.Formatter):
    """Custom formatter for Stripe logs with structured fields."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with timestamp, user_id, and request_id.

        Args:
            record: Log record to format

        Returns:
            Formatted log string
        """
        # Add timestamp
        record.timestamp = datetime.utcnow().isoformat()

        # Add user_id if available
        if not hasattr(record, 'user_id'):
            record.user_id = None

        # Add request_id if available
        if not hasattr(record, 'request_id'):
            record.request_id = None

        # Format the message
        log_data = {
            'timestamp': record.timestamp,
            'level': record.levelname,
            'user_id': record.user_id,
            'request_id': record.request_id,
            'message': record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, 'event_type'):
            log_data['event_type'] = record.event_type
        if hasattr(record, 'status'):
            log_data['status'] = record.status
        if hasattr(record, 'metadata'):
            log_data['metadata'] = record.metadata

        return json.dumps(log_data)


def _sanitize_value(value: Any) -> Any:
    """
    Sanitize a value to remove sensitive data.

    Args:
        value: Value to sanitize

    Returns:
        Sanitized value
    """
    if isinstance(value, str):
        # Sanitize credit card numbers (any 13-19 digit sequence)
        value = re.sub(r'\b\d{13,19}\b', '[CARD_NUMBER_REDACTED]', value)

        # Sanitize CVV/CVC (3-4 digit codes)
        value = re.sub(r'\b\d{3,4}\b(?=.*(?:cvv|cvc|security))', '[CVV_REDACTED]', value, flags=re.IGNORECASE)

        # Sanitize API keys and secrets
        if any(keyword in value.lower() for keyword in ['secret', 'api_key', 'token', 'password']):
            if len(value) > 8:
                value = value[:4] + '[REDACTED]'

    elif isinstance(value, dict):
        return _sanitize_dict(value)
    elif isinstance(value, list):
        return [_sanitize_value(item) for item in value]

    return value


def _sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively sanitize a dictionary to remove sensitive data.

    Redacts fields containing: card numbers, CVV, API keys, secrets, tokens.

    Args:
        data: Dictionary to sanitize

    Returns:
        Sanitized dictionary
    """
    sensitive_fields = {
        'number', 'card_number', 'cvv', 'cvc', 'security_code',
        'secret', 'api_key', 'token', 'password', 'client_secret',
        'exp_month', 'exp_year', 'ssn', 'bank_account'
    }

    sanitized = {}
    for key, value in data.items():
        # Check if field name indicates sensitive data
        if any(sensitive in key.lower() for sensitive in sensitive_fields):
            sanitized[key] = '[REDACTED]'
        else:
            sanitized[key] = _sanitize_value(value)

    return sanitized


def log_stripe_event(
    event_type: str,
    status: str,
    metadata: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
    level: str = 'info'
) -> None:
    """
    Log a Stripe event with structured data.

    Args:
        event_type: Type of Stripe event (e.g., 'payment_intent.created',
                   'subscription.updated', 'checkout_session.completed')
        status: Status of the event (e.g., 'success', 'failed', 'pending')
        metadata: Additional metadata about the event
        user_id: ID of the user associated with the event
        request_id: Request ID for tracing
        level: Log level ('debug', 'info', 'warning', 'error')
    """
    # Sanitize metadata
    sanitized_metadata = _sanitize_dict(metadata) if metadata else {}

    # Create log record with extra fields
    log_func = getattr(logger, level.lower(), logger.info)

    message = f"Stripe event: {event_type} - {status}"

    # Log with extra fields
    log_func(
        message,
        extra={
            'event_type': event_type,
            'status': status,
            'metadata': sanitized_metadata,
            'user_id': user_id,
            'request_id': request_id
        }
    )


def log_stripe_error(
    error: Exception,
    event_type: str,
    context: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None
) -> None:
    """
    Log a Stripe error with full context.

    Args:
        error: The exception that occurred
        event_type: Type of operation that failed (e.g., 'create_payment_intent',
                   'create_subscription', 'process_webhook')
        context: Additional context about the error (operation parameters, state)
        user_id: ID of the user associated with the error
        request_id: Request ID for tracing
    """
    # Sanitize context
    sanitized_context = _sanitize_dict(context) if context else {}

    # Extract error details
    error_type = type(error).__name__
    error_message = str(error)

    # For Stripe errors, extract additional details
    error_code = getattr(error, 'code', None)
    error_param = getattr(error, 'param', None)
    http_status = getattr(error, 'http_status', None)

    metadata = {
        'error_type': error_type,
        'error_message': _sanitize_value(error_message),
        'context': sanitized_context
    }

    if error_code:
        metadata['error_code'] = error_code
    if error_param:
        metadata['error_param'] = error_param
    if http_status:
        metadata['http_status'] = http_status

    # Log error
    logger.error(
        f"Stripe error in {event_type}: {error_type}",
        extra={
            'event_type': event_type,
            'status': 'error',
            'metadata': metadata,
            'user_id': user_id,
            'request_id': request_id
        },
        exc_info=True
    )


def configure_stripe_logging(
    log_level: str = 'INFO',
    log_file: Optional[str] = None
) -> None:
    """
    Configure logging for Stripe operations.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for log output
    """
    # Set log level
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = StripeLogFormatter()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False
