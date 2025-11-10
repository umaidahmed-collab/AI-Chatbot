"""
Blog posts router.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import BlogPost as BlogPostModel, Author as AuthorModel
from app.models.schemas import BlogPost, Author
from app.services.database import get_db

router = APIRouter()


@router.get("/", response_model=List[BlogPost])
async def get_posts(
    limit: int = Query(default=10, ge=1, le=100, description="Number of posts to return"),
    offset: int = Query(default=0, ge=0, description="Number of posts to skip"),
    db: Session = Depends(get_db)
):
    """Get list of blog posts with pagination support."""
    posts = (
        db.query(BlogPostModel)
        .order_by(BlogPostModel.publication_date.desc(), BlogPostModel.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return posts


@router.get("/{post_id}", response_model=BlogPost)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Get a single blog post by ID with full content."""
    post = db.query(BlogPostModel).filter(BlogPostModel.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    return post


@router.get("/authors/{author_id}", response_model=Author)
async def get_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    """Get author details by ID."""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author
