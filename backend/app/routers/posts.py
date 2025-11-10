"""
Posts router for blog API.

This module provides CRUD endpoints for managing blog posts with:
- Create post with validation
- List posts with pagination and filtering
- Get individual post by ID
- Update post with validation
- Delete post with authorization

All endpoints use the Post and Author database models defined in app.models.database.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.models.database import Post, Author, User
from app.models.schemas import (
    PostCreate,
    PostUpdate,
    Post as PostSchema,
    PaginatedPostsResponse,
    PostStatus
)
from app.services.database import get_db
from app.services.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new blog post.

    Args:
        post: PostCreate schema with author_id, title, content, and optional status
        db: Database session
        current_user: Authenticated user (required for authorization)

    Returns:
        PostSchema: Created post with all attributes including author relationship

    Raises:
        HTTPException 400: If author_id does not exist
        HTTPException 401: If user is not authenticated

    Example:
        POST /api/posts
        {
            "author_id": 1,
            "title": "My First Blog Post",
            "content": "This is the content of my blog post.",
            "status": "draft"
        }
    """
    # Validate that author exists
    author = db.query(Author).filter(Author.id == post.author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Author with id {post.author_id} not found"
        )

    # Create new post
    db_post = Post(
        author_id=post.author_id,
        title=post.title,
        content=post.content,
        status=post.status
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@router.get("/", response_model=PaginatedPostsResponse)
async def list_posts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    status: Optional[PostStatus] = Query(None, description="Filter by post status (draft, published, archived)"),
    author_id: Optional[int] = Query(None, description="Filter by author ID"),
    db: Session = Depends(get_db)
):
    """
    List blog posts with pagination and filtering.

    Args:
        skip: Number of records to skip (for pagination), default 0
        limit: Maximum number of records to return (1-100), default 10
        status: Optional filter by post status (draft, published, archived)
        author_id: Optional filter by author ID
        db: Database session

    Returns:
        PaginatedPostsResponse: Paginated list of posts with metadata
            - total: Total number of posts matching filters
            - page: Current page number
            - page_size: Number of items per page
            - total_pages: Total number of pages
            - items: List of posts for current page

    Example:
        GET /api/posts?skip=0&limit=10&status=published&author_id=1
    """
    # Build query with filters
    query = db.query(Post)

    if status:
        query = query.filter(Post.status == status)

    if author_id:
        query = query.filter(Post.author_id == author_id)

    # Get total count for pagination
    total = query.count()

    # Apply pagination and fetch results
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

    # Calculate pagination metadata
    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = (total + limit - 1) // limit if limit > 0 else 1

    return PaginatedPostsResponse(
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages,
        items=posts
    )


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single blog post by ID.

    Args:
        post_id: ID of the post to retrieve
        db: Database session

    Returns:
        PostSchema: Post with all attributes including author relationship

    Raises:
        HTTPException 404: If post with given ID does not exist

    Example:
        GET /api/posts/1
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    return post


@router.put("/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing blog post.

    Args:
        post_id: ID of the post to update
        post_update: PostUpdate schema with optional fields to update
        db: Database session
        current_user: Authenticated user (required for authorization)

    Returns:
        PostSchema: Updated post with all attributes

    Raises:
        HTTPException 404: If post with given ID does not exist
        HTTPException 400: If author_id is provided but does not exist
        HTTPException 401: If user is not authenticated

    Example:
        PUT /api/posts/1
        {
            "title": "Updated Title",
            "status": "published"
        }

    Note:
        Only provided fields will be updated. Omitted fields remain unchanged.
    """
    # Check if post exists
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    # If author_id is being updated, validate it exists
    if post_update.author_id is not None:
        author = db.query(Author).filter(Author.id == post_update.author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Author with id {post_update.author_id} not found"
            )

    # Update only provided fields
    update_data = post_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_post, field, value)

    db.commit()
    db.refresh(db_post)

    return db_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a blog post.

    Args:
        post_id: ID of the post to delete
        db: Database session
        current_user: Authenticated user (required for authorization)

    Returns:
        None (204 No Content on success)

    Raises:
        HTTPException 404: If post with given ID does not exist
        HTTPException 401: If user is not authenticated

    Example:
        DELETE /api/posts/1

    Note:
        This operation is permanent and cannot be undone.
        Requires authentication to prevent unauthorized deletions.
    """
    # Check if post exists
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    # Delete the post
    db.delete(db_post)
    db.commit()

    return None
