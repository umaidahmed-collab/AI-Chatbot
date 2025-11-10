"""
Authors router for blog API.

This module provides endpoints for managing and retrieving blog authors with:
- List all authors
- Get individual author by ID with their posts

All endpoints use the Author database model defined in app.models.database.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import Author
from app.models.schemas import Author as AuthorSchema, AuthorWithPosts
from app.services.database import get_db

router = APIRouter()


@router.get("/", response_model=list[AuthorSchema])
async def list_authors(db: Session = Depends(get_db)):
    """
    List all blog authors.

    Args:
        db: Database session

    Returns:
        list[AuthorSchema]: List of all authors with their basic information

    Example:
        GET /api/authors

        Response:
        [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "bio": "Technology writer and software developer",
                "created_at": "2025-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "bio": "Content strategist and blogger",
                "created_at": "2025-01-16T14:20:00Z"
            }
        ]
    """
    authors = db.query(Author).order_by(Author.created_at.desc()).all()
    return authors


@router.get("/{author_id}", response_model=AuthorWithPosts)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Get a single author by ID including all their posts.

    Args:
        author_id: ID of the author to retrieve
        db: Database session

    Returns:
        AuthorWithPosts: Author with all attributes including their posts

    Raises:
        HTTPException 404: If author with given ID does not exist

    Example:
        GET /api/authors/1

        Response:
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "Technology writer and software developer",
            "created_at": "2025-01-15T10:30:00Z",
            "posts": [
                {
                    "id": 1,
                    "title": "Getting Started with FastAPI",
                    "content": "FastAPI is a modern web framework...",
                    "status": "published",
                    "author_id": 1,
                    "created_at": "2025-01-20T09:00:00Z",
                    "updated_at": null,
                    "author": null
                },
                {
                    "id": 2,
                    "title": "Python Best Practices",
                    "content": "Writing clean Python code...",
                    "status": "published",
                    "author_id": 1,
                    "created_at": "2025-01-22T11:30:00Z",
                    "updated_at": null,
                    "author": null
                }
            ]
        }
    """
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found"
        )

    return author
