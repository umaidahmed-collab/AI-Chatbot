"""
Application configuration settings.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "postgresql://chatbot:password@localhost:5432/chatbot_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = ""

    # SendGrid Email Configuration
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = "noreply@example.com"
    SENDGRID_FROM_NAME: str = "AI Chatbot"

    # Email Template Settings
    EMAIL_LOGO_URL: str = "https://example.com/logo.png"
    EMAIL_BRAND_PRIMARY_COLOR: str = "#4F46E5"
    EMAIL_BRAND_SECONDARY_COLOR: str = "#6366F1"
    EMAIL_COMPANY_NAME: str = "AI Chatbot Inc."
    EMAIL_SUPPORT_EMAIL: str = "support@example.com"

    # Receipt Settings
    RECEIPT_PDF_ENABLED: bool = True
    RECEIPT_URL_BASE: str = "https://example.com/receipts"
    RECEIPT_STORAGE_PATH: str = "receipts"

    # Email Retry Policy
    EMAIL_MAX_RETRIES: int = 3
    EMAIL_RETRY_DELAYS: List[int] = [1, 5, 15]  # seconds between retries
    EMAIL_RETRY_EXPONENTIAL_BACKOFF: bool = True

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # File uploads
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".txt", ".docx"]
    
    # ChromaDB
    CHROMA_DB_PATH: str = "chroma_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
