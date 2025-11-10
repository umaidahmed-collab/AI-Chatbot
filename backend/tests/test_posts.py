"""
Unit tests for blog posts API endpoints.

This module tests CRUD operations on the /api/posts endpoints including:
- Creating posts with validation
- Listing posts with pagination and filtering
- Getting individual posts
- Updating posts
- Deleting posts
- Error handling for various edge cases
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.database import Author, Post, PostStatus


@pytest.fixture
def test_author(db: Session):
    """Create a test author fixture."""
    author = Author(
        name="Test Author",
        email="author@example.com",
        bio="This is a test author bio"
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@pytest.fixture
def test_author_2(db: Session):
    """Create a second test author fixture."""
    author = Author(
        name="Second Author",
        email="author2@example.com",
        bio="This is the second test author"
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@pytest.fixture
def test_post(db: Session, test_author: Author):
    """Create a test post fixture."""
    post = Post(
        author_id=test_author.id,
        title="Test Post",
        content="This is test post content",
        status=PostStatus.draft
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@pytest.fixture
def test_posts(db: Session, test_author: Author, test_author_2: Author):
    """Create multiple test posts for pagination and filtering tests."""
    posts = [
        Post(
            author_id=test_author.id,
            title="Draft Post 1",
            content="Content of draft post 1",
            status=PostStatus.draft
        ),
        Post(
            author_id=test_author.id,
            title="Published Post 1",
            content="Content of published post 1",
            status=PostStatus.published
        ),
        Post(
            author_id=test_author_2.id,
            title="Published Post 2",
            content="Content of published post 2",
            status=PostStatus.published
        ),
        Post(
            author_id=test_author.id,
            title="Archived Post 1",
            content="Content of archived post 1",
            status=PostStatus.archived
        ),
        Post(
            author_id=test_author_2.id,
            title="Draft Post 2",
            content="Content of draft post 2",
            status=PostStatus.draft
        ),
    ]

    for post in posts:
        db.add(post)

    db.commit()

    for post in posts:
        db.refresh(post)

    return posts


# ============================================================================
# POST /api/posts - Create Post Tests
# ============================================================================

def test_create_post(authenticated_client: TestClient, test_author: Author):
    """Test creating a new blog post."""
    post_data = {
        "author_id": test_author.id,
        "title": "New Blog Post",
        "content": "This is the content of my new blog post.",
        "status": "draft"
    }

    response = authenticated_client.post("/api/posts/", json=post_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
    assert data["status"] == post_data["status"]
    assert data["author_id"] == test_author.id
    assert "id" in data
    assert "created_at" in data
    assert data["author"]["name"] == test_author.name
    assert data["author"]["email"] == test_author.email


def test_create_post_default_status(authenticated_client: TestClient, test_author: Author):
    """Test creating a post without specifying status (should default to draft)."""
    post_data = {
        "author_id": test_author.id,
        "title": "New Post Without Status",
        "content": "Content without explicit status"
    }

    response = authenticated_client.post("/api/posts/", json=post_data)

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "draft"


def test_create_post_nonexistent_author(authenticated_client: TestClient):
    """Test creating a post with non-existent author ID."""
    post_data = {
        "author_id": 99999,
        "title": "Post with Invalid Author",
        "content": "This should fail"
    }

    response = authenticated_client.post("/api/posts/", json=post_data)

    assert response.status_code == 400
    assert "Author with id 99999 not found" in response.json()["detail"]


def test_create_post_unauthorized(client: TestClient, test_author: Author):
    """Test creating a post without authentication."""
    post_data = {
        "author_id": test_author.id,
        "title": "Unauthorized Post",
        "content": "This should fail"
    }

    response = client.post("/api/posts/", json=post_data)

    assert response.status_code == 401


def test_create_post_invalid_data(authenticated_client: TestClient, test_author: Author):
    """Test creating a post with invalid data (missing required fields)."""
    post_data = {
        "author_id": test_author.id,
        # Missing title and content
    }

    response = authenticated_client.post("/api/posts/", json=post_data)

    assert response.status_code == 422  # Validation error


def test_create_post_empty_title(authenticated_client: TestClient, test_author: Author):
    """Test creating a post with empty title."""
    post_data = {
        "author_id": test_author.id,
        "title": "",
        "content": "Content here"
    }

    response = authenticated_client.post("/api/posts/", json=post_data)

    assert response.status_code == 422  # Validation error


# ============================================================================
# GET /api/posts - List Posts Tests
# ============================================================================

def test_list_posts(client: TestClient, test_posts: list):
    """Test listing all posts with default pagination."""
    response = client.get("/api/posts/")

    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data
    assert "items" in data
    assert data["total"] == len(test_posts)
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) == len(test_posts)


def test_list_posts_pagination(client: TestClient, test_posts: list):
    """Test listing posts with custom pagination."""
    response = client.get("/api/posts/?skip=0&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == len(test_posts)
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) == 2
    assert data["total_pages"] == 3  # 5 posts / 2 per page = 3 pages


def test_list_posts_second_page(client: TestClient, test_posts: list):
    """Test listing posts on second page."""
    response = client.get("/api/posts/?skip=2&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert len(data["items"]) == 2


def test_list_posts_filter_by_status(client: TestClient, test_posts: list):
    """Test filtering posts by status."""
    response = client.get("/api/posts/?status=published")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # Two published posts in test_posts
    assert all(post["status"] == "published" for post in data["items"])


def test_list_posts_filter_by_author(client: TestClient, test_posts: list, test_author: Author):
    """Test filtering posts by author ID."""
    response = client.get(f"/api/posts/?author_id={test_author.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3  # test_author has 3 posts in test_posts
    assert all(post["author_id"] == test_author.id for post in data["items"])


def test_list_posts_filter_by_status_and_author(
    client: TestClient,
    test_posts: list,
    test_author: Author
):
    """Test filtering posts by both status and author."""
    response = client.get(f"/api/posts/?status=published&author_id={test_author.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1  # Only one published post by test_author
    assert all(
        post["status"] == "published" and post["author_id"] == test_author.id
        for post in data["items"]
    )


def test_list_posts_empty(client: TestClient):
    """Test listing posts when no posts exist."""
    response = client.get("/api/posts/")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_list_posts_ordered_by_created_at(client: TestClient, test_posts: list):
    """Test that posts are ordered by created_at descending (newest first)."""
    response = client.get("/api/posts/")

    assert response.status_code == 200
    data = response.json()
    items = data["items"]

    # Verify items are in descending order by created_at
    for i in range(len(items) - 1):
        assert items[i]["created_at"] >= items[i + 1]["created_at"]


# ============================================================================
# GET /api/posts/{post_id} - Get Single Post Tests
# ============================================================================

def test_get_post(client: TestClient, test_post: Post):
    """Test getting a single post by ID."""
    response = client.get(f"/api/posts/{test_post.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == test_post.title
    assert data["content"] == test_post.content
    assert data["status"] == test_post.status.value
    assert data["author_id"] == test_post.author_id
    assert "author" in data
    assert data["author"]["name"] == test_post.author.name


def test_get_post_not_found(client: TestClient):
    """Test getting a post that doesn't exist."""
    response = client.get("/api/posts/99999")

    assert response.status_code == 404
    assert "Post with id 99999 not found" in response.json()["detail"]


# ============================================================================
# PUT /api/posts/{post_id} - Update Post Tests
# ============================================================================

def test_update_post(authenticated_client: TestClient, test_post: Post):
    """Test updating a post."""
    update_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "status": "published"
    }

    response = authenticated_client.put(f"/api/posts/{test_post.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == update_data["title"]
    assert data["content"] == update_data["content"]
    assert data["status"] == update_data["status"]
    assert data["author_id"] == test_post.author_id  # Author unchanged


def test_update_post_partial(authenticated_client: TestClient, test_post: Post):
    """Test partially updating a post (only some fields)."""
    original_content = test_post.content
    update_data = {
        "title": "Only Title Updated"
    }

    response = authenticated_client.put(f"/api/posts/{test_post.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["content"] == original_content  # Content unchanged


def test_update_post_status_only(authenticated_client: TestClient, test_post: Post):
    """Test updating only the post status."""
    update_data = {
        "status": "published"
    }

    response = authenticated_client.put(f"/api/posts/{test_post.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "published"
    assert data["title"] == test_post.title


def test_update_post_change_author(
    authenticated_client: TestClient,
    test_post: Post,
    test_author_2: Author
):
    """Test updating a post to change its author."""
    update_data = {
        "author_id": test_author_2.id
    }

    response = authenticated_client.put(f"/api/posts/{test_post.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["author_id"] == test_author_2.id
    assert data["author"]["name"] == test_author_2.name


def test_update_post_nonexistent_author(authenticated_client: TestClient, test_post: Post):
    """Test updating a post with non-existent author ID."""
    update_data = {
        "author_id": 99999
    }

    response = authenticated_client.put(f"/api/posts/{test_post.id}", json=update_data)

    assert response.status_code == 400
    assert "Author with id 99999 not found" in response.json()["detail"]


def test_update_post_not_found(authenticated_client: TestClient):
    """Test updating a post that doesn't exist."""
    update_data = {
        "title": "Updated Title"
    }

    response = authenticated_client.put("/api/posts/99999", json=update_data)

    assert response.status_code == 404
    assert "Post with id 99999 not found" in response.json()["detail"]


def test_update_post_unauthorized(client: TestClient, test_post: Post):
    """Test updating a post without authentication."""
    update_data = {
        "title": "Should Fail"
    }

    response = client.put(f"/api/posts/{test_post.id}", json=update_data)

    assert response.status_code == 401


def test_update_post_invalid_data(authenticated_client: TestClient, test_post: Post):
    """Test updating a post with invalid data (empty title)."""
    update_data = {
        "title": ""  # Empty title should fail validation
    }

    response = authenticated_client.put(f"/api/posts/{test_post.id}", json=update_data)

    assert response.status_code == 422  # Validation error


# ============================================================================
# DELETE /api/posts/{post_id} - Delete Post Tests
# ============================================================================

def test_delete_post(authenticated_client: TestClient, test_post: Post):
    """Test deleting a post."""
    response = authenticated_client.delete(f"/api/posts/{test_post.id}")

    assert response.status_code == 204

    # Verify post is deleted
    get_response = authenticated_client.get(f"/api/posts/{test_post.id}")
    assert get_response.status_code == 404


def test_delete_post_not_found(authenticated_client: TestClient):
    """Test deleting a post that doesn't exist."""
    response = authenticated_client.delete("/api/posts/99999")

    assert response.status_code == 404
    assert "Post with id 99999 not found" in response.json()["detail"]


def test_delete_post_unauthorized(client: TestClient, test_post: Post):
    """Test deleting a post without authentication."""
    response = client.delete(f"/api/posts/{test_post.id}")

    assert response.status_code == 401


def test_delete_post_verify_cascade(
    authenticated_client: TestClient,
    db: Session,
    test_post: Post
):
    """Test that deleting a post doesn't affect the author."""
    author_id = test_post.author_id
    post_id = test_post.id

    response = authenticated_client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 204

    # Verify author still exists
    author = db.query(Author).filter(Author.id == author_id).first()
    assert author is not None
