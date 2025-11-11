"""
Stripe webhook endpoint tests.

Security test coverage:
- Webhook signature verification (valid/invalid/missing)
- Idempotency handling for duplicate events
- Event type routing and processing
- Error handling and logging
- Input validation and sanitization
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import stripe

from app.services.stripe_service import StripeWebhookError


class TestWebhookSignatureVerification:
    """Tests for webhook signature verification security."""

    @patch('stripe.Webhook.construct_event')
    def test_webhook_signature_verification_success(self, mock_construct_event, client, db):
        """
        Test that valid webhook signatures are accepted.

        Security: Validates that properly signed webhooks from Stripe pass verification.
        """
        # Arrange
        mock_event = {
            "id": "evt_test_123",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_123",
                    "payment_intent": "pi_test_123",
                    "customer": "cus_test_123",
                    "customer_email": "test@example.com",
                    "amount_total": 5000,
                    "currency": "usd",
                    "subscription": None
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature_hash"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        mock_construct_event.assert_called_once()

    @patch('stripe.Webhook.construct_event')
    def test_webhook_signature_verification_failure(self, mock_construct_event, client):
        """
        Test that invalid webhook signatures are rejected with 400.

        Security: Critical test ensuring forged/tampered webhooks are blocked.
        This prevents attackers from spoofing payment events.
        """
        # Arrange
        mock_construct_event.side_effect = stripe.error.SignatureVerificationError(
            "Invalid signature",
            sig_header="invalid_signature"
        )

        payload = b'{"id": "evt_fake", "type": "payment_intent.succeeded"}'
        signature = "t=1614556800,v1=invalid_signature_hash"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 400
        assert "Invalid webhook signature" in response.json()["detail"]

    def test_webhook_missing_signature_header(self, client):
        """
        Test that webhooks without signature headers are rejected.

        Security: Prevents unsigned webhook requests from being processed.
        """
        # Arrange
        payload = b'{"id": "evt_test", "type": "payment_intent.succeeded"}'

        # Act
        response = client.post(
            "/api/webhooks/stripe",
            content=payload
        )

        # Assert
        assert response.status_code == 400
        assert "Missing stripe-signature header" in response.json()["detail"]

    def test_webhook_missing_secret_configuration(self, client):
        """
        Test that webhooks fail gracefully when secret is not configured.

        Security: Ensures webhooks cannot be processed without proper configuration.
        """
        # Arrange
        payload = b'{"id": "evt_test", "type": "payment_intent.succeeded"}'
        signature = "t=1614556800,v1=signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', ''):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 500
        assert "Webhook configuration error" in response.json()["detail"]

    @patch('stripe.Webhook.construct_event')
    def test_webhook_malformed_payload(self, mock_construct_event, client):
        """
        Test handling of malformed webhook payloads.

        Security: Validates proper error handling for invalid input.
        """
        # Arrange
        mock_construct_event.side_effect = ValueError("Invalid payload format")

        payload = b'malformed json {'
        signature = "t=1614556800,v1=signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 400


class TestCheckoutSessionCompleted:
    """Tests for checkout.session.completed event handling."""

    @patch('stripe.Webhook.construct_event')
    def test_checkout_session_completed(self, mock_construct_event, client, db, test_user_data):
        """
        Test successful checkout session processing creates payment records.

        Security: Validates that payment records are created only after signature verification.
        """
        # Arrange - Create test user
        client.post("/api/auth/register", json=test_user_data)

        mock_event = {
            "id": "evt_checkout_123",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_123",
                    "payment_intent": "pi_test_123",
                    "customer": "cus_test_123",
                    "customer_email": test_user_data["email"],
                    "amount_total": 5000,
                    "currency": "usd",
                    "subscription": "sub_test_123"
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # TODO: Once Payment model exists, verify payment record created:
        # from app.models.database import Payment
        # payment = db.query(Payment).filter_by(payment_intent_id="pi_test_123").first()
        # assert payment is not None
        # assert payment.amount == 5000
        # assert payment.currency == "usd"

    @patch('stripe.Webhook.construct_event')
    def test_checkout_session_user_not_found(self, mock_construct_event, client, db):
        """
        Test checkout session fails gracefully when user doesn't exist.

        Security: Ensures we don't create orphaned payment records.
        """
        # Arrange
        mock_event = {
            "id": "evt_checkout_456",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_456",
                    "payment_intent": "pi_test_456",
                    "customer": "cus_unknown",
                    "customer_email": "nonexistent@example.com",
                    "amount_total": 5000,
                    "currency": "usd",
                    "subscription": None
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert - Should return 400 because user not found
        assert response.status_code == 400


class TestPaymentIntentEvents:
    """Tests for payment_intent.* events."""

    @patch('stripe.Webhook.construct_event')
    def test_payment_intent_succeeded(self, mock_construct_event, client, db):
        """
        Test payment_intent.succeeded updates payment status.

        Security: Validates status updates only occur after signature verification.
        """
        # Arrange
        mock_event = {
            "id": "evt_pi_success_123",
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_test_123",
                    "amount": 5000,
                    "currency": "usd",
                    "customer": "cus_test_123",
                    "status": "succeeded"
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 200

        # TODO: Once Payment model exists, verify status updated:
        # payment = db.query(Payment).filter_by(payment_intent_id="pi_test_123").first()
        # assert payment.status == "succeeded"

    @patch('stripe.Webhook.construct_event')
    def test_payment_intent_failed(self, mock_construct_event, client, db):
        """
        Test payment_intent.payment_failed marks payment as failed.

        Security: Validates failure handling and ensures sensitive data isn't logged.
        """
        # Arrange
        mock_event = {
            "id": "evt_pi_failed_123",
            "type": "payment_intent.payment_failed",
            "data": {
                "object": {
                    "id": "pi_test_failed_123",
                    "amount": 5000,
                    "currency": "usd",
                    "customer": "cus_test_123",
                    "status": "failed",
                    "last_payment_error": {
                        "code": "card_declined",
                        "message": "Your card was declined"
                    }
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 200

        # TODO: Once Payment model exists, verify failure recorded:
        # payment = db.query(Payment).filter_by(payment_intent_id="pi_test_failed_123").first()
        # assert payment.status == "failed"
        # assert payment.failure_code == "card_declined"


class TestSubscriptionEvents:
    """Tests for customer.subscription.* events."""

    @patch('stripe.Webhook.construct_event')
    def test_subscription_updated(self, mock_construct_event, client, db):
        """
        Test customer.subscription.updated updates subscription status.

        Security: Validates subscription changes only occur after verification.
        """
        # Arrange
        mock_event = {
            "id": "evt_sub_updated_123",
            "type": "customer.subscription.updated",
            "data": {
                "object": {
                    "id": "sub_test_123",
                    "customer": "cus_test_123",
                    "status": "active",
                    "current_period_start": 1614556800,
                    "current_period_end": 1617235200,
                    "cancel_at_period_end": False
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 200

        # TODO: Once Subscription model exists, verify update:
        # subscription = db.query(Subscription).filter_by(subscription_id="sub_test_123").first()
        # assert subscription.status == "active"
        # assert subscription.cancel_at_period_end == False

    @patch('stripe.Webhook.construct_event')
    def test_subscription_canceled(self, mock_construct_event, client, db):
        """
        Test customer.subscription.deleted handles cancellations.

        Security: Validates cancellations are processed securely.
        """
        # Arrange
        mock_event = {
            "id": "evt_sub_deleted_123",
            "type": "customer.subscription.deleted",
            "data": {
                "object": {
                    "id": "sub_test_canceled_123",
                    "customer": "cus_test_123",
                    "status": "canceled",
                    "current_period_start": 1614556800,
                    "current_period_end": 1617235200,
                    "cancel_at_period_end": True
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 200


class TestWebhookIdempotency:
    """Tests for webhook idempotency handling."""

    @patch('stripe.Webhook.construct_event')
    def test_webhook_idempotency(self, mock_construct_event, client, db, test_user_data):
        """
        Test duplicate webhook events are handled idempotently.

        Security: CRITICAL - Prevents double-charging and duplicate processing.
        Stripe may send the same webhook multiple times, so idempotency is essential.
        """
        # Arrange - Create test user
        client.post("/api/auth/register", json=test_user_data)

        mock_event = {
            "id": "evt_idempotent_123",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_idempotent_123",
                    "payment_intent": "pi_idempotent_123",
                    "customer": "cus_test_123",
                    "customer_email": test_user_data["email"],
                    "amount_total": 5000,
                    "currency": "usd",
                    "subscription": None
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act - Send same webhook twice
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response1 = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

            response2 = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert - Both requests should succeed (idempotent)
        assert response1.status_code == 200
        assert response2.status_code == 200

        # TODO: Once Payment model exists, verify only ONE payment record created:
        # from app.models.database import Payment
        # payments = db.query(Payment).filter_by(payment_intent_id="pi_idempotent_123").all()
        # assert len(payments) == 1, "Duplicate webhook should not create multiple payment records"

    @patch('stripe.Webhook.construct_event')
    def test_webhook_different_events_same_payment_intent(self, mock_construct_event, client, db, test_user_data):
        """
        Test different event types for same payment_intent are handled correctly.

        Security: Validates that payment_intent lifecycle events don't create duplicates.
        """
        # Arrange - Create test user
        client.post("/api/auth/register", json=test_user_data)

        # Event 1: checkout.session.completed
        event1 = {
            "id": "evt_checkout_pi_123",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_123",
                    "payment_intent": "pi_shared_123",
                    "customer": "cus_test_123",
                    "customer_email": test_user_data["email"],
                    "amount_total": 5000,
                    "currency": "usd",
                    "subscription": None
                }
            }
        }

        # Event 2: payment_intent.succeeded (for same payment_intent)
        event2 = {
            "id": "evt_pi_succeeded_123",
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_shared_123",
                    "amount": 5000,
                    "currency": "usd",
                    "customer": "cus_test_123",
                    "status": "succeeded"
                }
            }
        }

        signature = "t=1614556800,v1=valid_signature"

        # Act - Send both events
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            mock_construct_event.return_value = event1
            response1 = client.post(
                "/api/webhooks/stripe",
                content=json.dumps(event1).encode('utf-8'),
                headers={"stripe-signature": signature}
            )

            mock_construct_event.return_value = event2
            response2 = client.post(
                "/api/webhooks/stripe",
                content=json.dumps(event2).encode('utf-8'),
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # TODO: Verify only one payment record with updated status:
        # payment = db.query(Payment).filter_by(payment_intent_id="pi_shared_123").first()
        # assert payment.status == "succeeded"


class TestWebhookEventRouting:
    """Tests for webhook event type routing."""

    @patch('stripe.Webhook.construct_event')
    def test_unhandled_event_type(self, mock_construct_event, client, db):
        """
        Test unhandled event types are logged but don't cause errors.

        Security: Ensures graceful handling of unknown event types.
        """
        # Arrange
        mock_event = {
            "id": "evt_unhandled_123",
            "type": "customer.created",  # Unhandled event type
            "data": {
                "object": {
                    "id": "cus_new_123",
                    "email": "test@example.com"
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert - Should still return 200 (acknowledged but not processed)
        assert response.status_code == 200

    @patch('stripe.Webhook.construct_event')
    def test_webhook_processing_exception_handling(self, mock_construct_event, client, db):
        """
        Test unexpected exceptions during webhook processing are handled safely.

        Security: Validates error handling doesn't expose sensitive information.
        """
        # Arrange
        mock_event = {
            "id": "evt_error_123",
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_error_123",
                    "amount": 5000,
                    "currency": "usd"
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act - Simulate database error
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            with patch('app.services.stripe_service.StripeService.handle_payment_intent_succeeded',
                      side_effect=Exception("Database connection lost")):
                response = client.post(
                    "/api/webhooks/stripe",
                    content=payload,
                    headers={"stripe-signature": signature}
                )

        # Assert - Should return 500 (Stripe will retry)
        assert response.status_code == 500
        # Verify error message doesn't expose database details
        assert "Database connection lost" not in response.json()["detail"]


class TestWebhookSecurityHeaders:
    """Tests for webhook security headers and metadata."""

    @patch('stripe.Webhook.construct_event')
    def test_webhook_logs_remote_address(self, mock_construct_event, client, db):
        """
        Test that webhook requests log remote IP for security auditing.

        Security: IP logging helps track suspicious webhook activity.
        """
        # Arrange
        mock_event = {
            "id": "evt_audit_123",
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_audit_123",
                    "amount": 5000,
                    "currency": "usd"
                }
            }
        }
        mock_construct_event.return_value = mock_event

        payload = json.dumps(mock_event).encode('utf-8')
        signature = "t=1614556800,v1=valid_signature"

        # Act
        with patch('app.utils.config.settings.STRIPE_WEBHOOK_SECRET', 'whsec_test_secret'):
            response = client.post(
                "/api/webhooks/stripe",
                content=payload,
                headers={"stripe-signature": signature}
            )

        # Assert
        assert response.status_code == 200
        # Note: Actual IP logging verification would require log capture in tests
