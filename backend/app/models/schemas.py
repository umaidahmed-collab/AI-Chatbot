"""
Pydantic schemas for request/response models.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


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


# Blog schemas

# Post status enum
class PostStatus(str, Enum):
    """Post status enum for blog posts."""
    draft = "draft"
    published = "published"
    archived = "archived"


# Author schemas
class AuthorBase(BaseModel):
    """Base schema for Author with common attributes."""
    name: str = Field(..., min_length=1, max_length=100, description="Author's name")
    email: EmailStr = Field(..., description="Author's email address")
    bio: Optional[str] = Field(None, description="Author's biography")


class AuthorCreate(AuthorBase):
    """Schema for creating a new author."""
    pass


class Author(AuthorBase):
    """Schema for author responses with all attributes."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Post schemas
class PostBase(BaseModel):
    """Base schema for Post with common attributes."""
    title: str = Field(..., min_length=1, max_length=255, description="Post title")
    content: str = Field(..., min_length=1, description="Post content")
    status: PostStatus = Field(default=PostStatus.draft, description="Post status")


class PostCreate(PostBase):
    """Schema for creating a new post."""
    author_id: int = Field(..., description="ID of the post author")


class PostUpdate(BaseModel):
    """Schema for updating an existing post."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Post title")
    content: Optional[str] = Field(None, min_length=1, description="Post content")
    status: Optional[PostStatus] = Field(None, description="Post status")
    author_id: Optional[int] = Field(None, description="ID of the post author")


class Post(PostBase):
    """Schema for post responses with all attributes."""
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[Author] = None

    class Config:
        from_attributes = True


# Pagination and filtering schemas
class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number (starting from 1)")
    page_size: int = Field(default=10, ge=1, le=100, description="Number of items per page")


class PostFilterParams(BaseModel):
    """Schema for filtering posts."""
    status: Optional[PostStatus] = Field(None, description="Filter by post status")
    author_id: Optional[int] = Field(None, description="Filter by author ID")
    search: Optional[str] = Field(None, description="Search in title and content")


class PaginatedResponse(BaseModel):
    """Generic schema for paginated responses."""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")


class PaginatedPostsResponse(PaginatedResponse):
    """Schema for paginated posts response."""
    items: List[Post] = Field(..., description="List of posts for the current page")
