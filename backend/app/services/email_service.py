"""
Email service for sending emails via SendGrid.
"""

import logging
from typing import Optional, Dict, Any, List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from python_http_client.exceptions import HTTPError

from app.utils.config import settings


# Configure logging
logger = logging.getLogger(__name__)


class EmailServiceError(Exception):
    """Custom exception for email service errors."""
    pass


class EmailService:
    """Service for sending emails via SendGrid."""

    def __init__(self):
        """Initialize SendGrid client."""
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.SENDGRID_FROM_EMAIL
        self.from_name = settings.SENDGRID_FROM_NAME

        if not self.api_key:
            logger.warning("SendGrid API key not configured. Email functionality will be disabled.")
            self.client = None
        else:
            try:
                self.client = SendGridAPIClient(api_key=self.api_key)
                logger.info("SendGrid client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize SendGrid client: {str(e)}")
                self.client = None

    def _create_sendgrid_mail(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_text_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Mail:
        """
        Create a SendGrid Mail object.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            plain_text_content: Plain text content (optional)
            attachments: List of attachments with 'content', 'filename', 'type' keys

        Returns:
            Mail object ready to send
        """
        from_email_obj = Email(self.from_email, self.from_name)
        to_email_obj = To(to_email)

        # Create mail object
        mail = Mail(
            from_email=from_email_obj,
            to_emails=to_email_obj,
            subject=subject,
            html_content=html_content
        )

        # Add plain text content if provided
        if plain_text_content:
            mail.content = [
                Content("text/plain", plain_text_content),
                Content("text/html", html_content)
            ]

        # Add attachments if provided
        if attachments:
            for attachment_data in attachments:
                attachment = Attachment()
                attachment.file_content = FileContent(attachment_data['content'])
                attachment.file_name = FileName(attachment_data['filename'])
                attachment.file_type = FileType(attachment_data.get('type', 'application/octet-stream'))
                attachment.disposition = Disposition('attachment')
                mail.attachment = attachment

        return mail

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=15),
        retry=retry_if_exception_type((HTTPError, ConnectionError)),
        reraise=True
    )
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_text_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """
        Send an email via SendGrid with retry logic.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            plain_text_content: Plain text content (optional fallback)
            attachments: List of attachments with 'content', 'filename', 'type' keys

        Returns:
            True if email sent successfully, False otherwise

        Raises:
            EmailServiceError: If email sending fails after retries
        """
        if not self.client:
            error_msg = "SendGrid client not initialized. Cannot send email."
            logger.error(error_msg)
            raise EmailServiceError(error_msg)

        try:
            logger.info(f"Attempting to send email to {to_email} with subject: {subject}")

            # Create mail object
            mail = self._create_sendgrid_mail(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=plain_text_content,
                attachments=attachments
            )

            # Send email
            response = self.client.send(mail)

            # Check response status
            if response.status_code in [200, 201, 202]:
                logger.info(
                    f"Email sent successfully to {to_email}. "
                    f"Status code: {response.status_code}"
                )
                return True
            else:
                error_msg = (
                    f"Unexpected response from SendGrid. "
                    f"Status code: {response.status_code}, "
                    f"Body: {response.body}"
                )
                logger.warning(error_msg)
                raise EmailServiceError(error_msg)

        except HTTPError as e:
            error_msg = (
                f"SendGrid API error while sending email to {to_email}: "
                f"Status code: {e.status_code}, "
                f"Body: {e.body}, "
                f"Reason: {e.reason}"
            )
            logger.error(error_msg)
            raise EmailServiceError(error_msg) from e

        except ConnectionError as e:
            error_msg = f"Connection error while sending email to {to_email}: {str(e)}"
            logger.error(error_msg)
            raise EmailServiceError(error_msg) from e

        except Exception as e:
            error_msg = f"Unexpected error while sending email to {to_email}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise EmailServiceError(error_msg) from e

    async def send_receipt_email(
        self,
        to_email: str,
        receipt_data: Dict[str, Any],
        pdf_attachment: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a payment receipt email.

        Args:
            to_email: Recipient email address
            receipt_data: Dictionary containing receipt information
            pdf_attachment: Optional PDF attachment with 'content', 'filename' keys

        Returns:
            True if email sent successfully

        Raises:
            EmailServiceError: If email sending fails
        """
        subject = f"Receipt for Payment #{receipt_data.get('receipt_number', 'N/A')}"

        # Generate HTML content (will be enhanced with template in future)
        html_content = self._generate_receipt_html(receipt_data)
        plain_text_content = self._generate_receipt_plain_text(receipt_data)

        # Prepare attachments
        attachments = []
        if pdf_attachment:
            attachments.append(pdf_attachment)

        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            plain_text_content=plain_text_content,
            attachments=attachments if attachments else None
        )

    def _generate_receipt_html(self, receipt_data: Dict[str, Any]) -> str:
        """
        Generate HTML content for receipt email.

        Args:
            receipt_data: Dictionary containing receipt information

        Returns:
            HTML string
        """
        # Basic HTML template (will be enhanced with proper template in future)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Payment Receipt</title>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: {settings.EMAIL_BRAND_PRIMARY_COLOR}; color: white; padding: 20px; text-align: center;">
                <h1>Payment Receipt</h1>
            </div>
            <div style="padding: 20px; background-color: #f9f9f9;">
                <h2>Receipt #{receipt_data.get('receipt_number', 'N/A')}</h2>
                <p><strong>Date:</strong> {receipt_data.get('date', 'N/A')}</p>
                <p><strong>Amount:</strong> ${receipt_data.get('amount', '0.00')}</p>
                <p><strong>Payment Method:</strong> {receipt_data.get('payment_method', 'N/A')}</p>
                <p><strong>Status:</strong> {receipt_data.get('status', 'N/A')}</p>
            </div>
            <div style="padding: 20px; text-align: center; font-size: 12px; color: #666;">
                <p>Thank you for your payment!</p>
                <p>If you have any questions, please contact us at {settings.EMAIL_SUPPORT_EMAIL}</p>
                <p>&copy; {settings.EMAIL_COMPANY_NAME}</p>
            </div>
        </body>
        </html>
        """
        return html

    def _generate_receipt_plain_text(self, receipt_data: Dict[str, Any]) -> str:
        """
        Generate plain text content for receipt email.

        Args:
            receipt_data: Dictionary containing receipt information

        Returns:
            Plain text string
        """
        text = f"""
Payment Receipt

Receipt #: {receipt_data.get('receipt_number', 'N/A')}
Date: {receipt_data.get('date', 'N/A')}
Amount: ${receipt_data.get('amount', '0.00')}
Payment Method: {receipt_data.get('payment_method', 'N/A')}
Status: {receipt_data.get('status', 'N/A')}

Thank you for your payment!

If you have any questions, please contact us at {settings.EMAIL_SUPPORT_EMAIL}

{settings.EMAIL_COMPANY_NAME}
        """
        return text.strip()


# Create singleton instance
email_service = EmailService()
