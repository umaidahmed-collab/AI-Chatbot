"""
Database service and connection management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from app.models.database import Base, User, Document, ChatSession, ChatMessage, Author, BlogPost
from app.utils.config import settings
import asyncio


# Create synchronous engine
engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database tables."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


async def close_db():
    """Close database connections."""
    engine.dispose()
    print("Database connections closed!")
