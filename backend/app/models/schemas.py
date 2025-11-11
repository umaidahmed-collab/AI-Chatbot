"""
Pydantic schemas for request/response models.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Document schemas
class DocumentBase(BaseModel):
    filename: str
    original_filename: str


class DocumentCreate(DocumentBase):
    file_path: str
    file_size: int
    content_type: str


class Document(DocumentBase):
    id: int
    file_path: str
    file_size: int
    content_type: str
    processed: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Chat schemas
class ChatMessageBase(BaseModel):
    content: str
    role: str


class ChatMessageCreate(ChatMessageBase):
    session_id: int


class ChatMessage(ChatMessageBase):
    id: int
    session_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    title: Optional[str] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSession(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[ChatMessage] = []
    
    class Config:
        from_attributes = True


# Chat request/response schemas
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None
    use_documents: bool = True


class ChatResponse(BaseModel):
    message: str
    session_id: int
    sources: Optional[List[str]] = None


# Payment schemas
class PaymentBase(BaseModel):
    amount: Decimal = Field(..., description="Payment amount with decimal precision")
    currency: str = Field(default="usd", max_length=3, description="ISO 4217 currency code")
    payment_method: Optional[str] = Field(None, description="Payment method type (e.g., 'card', 'bank_transfer')")


class PaymentCreate(PaymentBase):
    stripe_payment_id: str = Field(..., description="Unique Stripe payment identifier")
    status: str = Field(..., description="Payment status (e.g., 'pending', 'succeeded', 'failed')")


class PaymentSchema(PaymentBase):
    """Complete payment schema for API responses."""
    id: int
    user_id: int
    stripe_payment_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Receipt data schemas
class ReceiptItem(BaseModel):
    """Individual item in a receipt."""
    description: str = Field(..., description="Item description")
    quantity: int = Field(..., gt=0, description="Quantity of items")
    unit_price: Decimal = Field(..., description="Price per unit")
    total_price: Decimal = Field(..., description="Total price for this item")


class ReceiptDataSchema(BaseModel):
    """Structured receipt information for email generation."""
    items: List[ReceiptItem] = Field(default_factory=list, description="List of purchased items")
    subtotal: Decimal = Field(..., description="Subtotal before taxes and fees")
    tax: Decimal = Field(default=Decimal("0.00"), description="Tax amount")
    fees: Decimal = Field(default=Decimal("0.00"), description="Additional fees")
    total: Decimal = Field(..., description="Total amount charged")
    currency: str = Field(default="usd", max_length=3, description="ISO 4217 currency code")
    payment_method: Optional[str] = Field(None, description="Payment method used")
    transaction_id: str = Field(..., description="Transaction/payment identifier")
    transaction_date: datetime = Field(..., description="Date and time of transaction")
    additional_info: Optional[Dict[str, Any]] = Field(default=None, description="Additional receipt metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "description": "Premium AI Chat Subscription",
                        "quantity": 1,
                        "unit_price": 29.99,
                        "total_price": 29.99
                    }
                ],
                "subtotal": 29.99,
                "tax": 2.70,
                "fees": 0.00,
                "total": 32.69,
                "currency": "usd",
                "payment_method": "card",
                "transaction_id": "pi_1234567890",
                "transaction_date": "2025-01-15T10:30:00Z"
            }
        }


# Email receipt schemas
class EmailReceiptBase(BaseModel):
    recipient_email: EmailStr = Field(..., description="Email address of the recipient")


class EmailReceiptCreate(EmailReceiptBase):
    payment_id: int = Field(..., description="Associated payment ID")


class EmailReceiptSchema(EmailReceiptBase):
    """Email receipt schema with delivery status fields."""
    id: int
    payment_id: int
    sent_at: Optional[datetime] = Field(None, description="Timestamp when email was successfully sent")
    status: str = Field(..., description="Email delivery status ('pending', 'sent', 'failed')")
    retry_count: int = Field(default=0, description="Number of delivery retry attempts")
    error_message: Optional[str] = Field(None, description="Error message if delivery failed")
    created_at: datetime = Field(..., description="Timestamp when email receipt record was created")

    class Config:
        from_attributes = True


class EmailReceiptWithPayment(EmailReceiptSchema):
    """Email receipt schema including payment details."""
    payment: PaymentSchema

    class Config:
        from_attributes = True
