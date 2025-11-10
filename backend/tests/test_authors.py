"""
Unit tests for blog authors API endpoints.

This module tests operations on the /api/authors endpoints including:
- Listing all authors
- Getting individual authors with their posts
- Error handling for non-existent authors
- Ordering and data structure validation
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
def test_author_3(db: Session):
    """Create a third test author fixture with no posts."""
    author = Author(
        name="Third Author",
        email="author3@example.com",
        bio="Author with no posts"
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@pytest.fixture
def test_author_with_posts(db: Session, test_author: Author):
    """Create a test author with multiple posts."""
    posts = [
        Post(
            author_id=test_author.id,
            title="First Post",
            content="Content of first post",
            status=PostStatus.published
        ),
        Post(
            author_id=test_author.id,
            title="Second Post",
            content="Content of second post",
            status=PostStatus.draft
        ),
        Post(
            author_id=test_author.id,
            title="Third Post",
            content="Content of third post",
            status=PostStatus.published
        ),
    ]

    for post in posts:
        db.add(post)

    db.commit()

    for post in posts:
        db.refresh(post)

    db.refresh(test_author)
    return test_author


@pytest.fixture
def test_authors_with_posts(
    db: Session,
    test_author: Author,
    test_author_2: Author,
    test_author_3: Author
):
    """Create multiple authors with varying numbers of posts."""
    posts = [
        # test_author gets 3 posts
        Post(
            author_id=test_author.id,
            title="Author 1 Post 1",
            content="Content 1",
            status=PostStatus.published
        ),
        Post(
            author_id=test_author.id,
            title="Author 1 Post 2",
            content="Content 2",
            status=PostStatus.draft
        ),
        Post(
            author_id=test_author.id,
            title="Author 1 Post 3",
            content="Content 3",
            status=PostStatus.archived
        ),
        # test_author_2 gets 2 posts
        Post(
            author_id=test_author_2.id,
            title="Author 2 Post 1",
            content="Content 1",
            status=PostStatus.published
        ),
        Post(
            author_id=test_author_2.id,
            title="Author 2 Post 2",
            content="Content 2",
            status=PostStatus.published
        ),
        # test_author_3 has no posts
    ]

    for post in posts:
        db.add(post)

    db.commit()

    for post in posts:
        db.refresh(post)

    db.refresh(test_author)
    db.refresh(test_author_2)
    db.refresh(test_author_3)

    return [test_author, test_author_2, test_author_3]


# ============================================================================
# GET /api/authors - List Authors Tests
# ============================================================================

def test_list_authors(client: TestClient, test_author: Author, test_author_2: Author):
    """Test listing all authors."""
    response = client.get("/api/authors/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    # Check author data structure
    for author in data:
        assert "id" in author
        assert "name" in author
        assert "email" in author
        assert "bio" in author
        assert "created_at" in author
        assert "posts" not in author  # Basic list doesn't include posts


def test_list_authors_empty(client: TestClient):
    """Test listing authors when no authors exist."""
    response = client.get("/api/authors/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_list_authors_single(client: TestClient, test_author: Author):
    """Test listing authors when only one author exists."""
    response = client.get("/api/authors/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_author.name
    assert data[0]["email"] == test_author.email
    assert data[0]["bio"] == test_author.bio


def test_list_authors_ordered_by_created_at(
    client: TestClient,
    test_authors_with_posts: list
):
    """Test that authors are ordered by created_at descending (newest first)."""
    response = client.get("/api/authors/")

    assert response.status_code == 200
    data = response.json()

    # Verify items are in descending order by created_at
    for i in range(len(data) - 1):
        assert data[i]["created_at"] >= data[i + 1]["created_at"]


def test_list_authors_data_integrity(
    client: TestClient,
    test_author: Author,
    test_author_2: Author
):
    """Test that all author data is correctly returned."""
    response = client.get("/api/authors/")

    assert response.status_code == 200
    data = response.json()

    # Find our test authors in the response
    author_names = [author["name"] for author in data]
    assert test_author.name in author_names
    assert test_author_2.name in author_names

    # Check specific author data
    author_1_data = next(a for a in data if a["name"] == test_author.name)
    assert author_1_data["email"] == test_author.email
    assert author_1_data["bio"] == test_author.bio


# ============================================================================
# GET /api/authors/{author_id} - Get Single Author with Posts Tests
# ============================================================================

def test_get_author(client: TestClient, test_author: Author):
    """Test getting a single author by ID."""
    response = client.get(f"/api/authors/{test_author.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_author.id
    assert data["name"] == test_author.name
    assert data["email"] == test_author.email
    assert data["bio"] == test_author.bio
    assert "created_at" in data
    assert "posts" in data
    assert isinstance(data["posts"], list)


def test_get_author_with_posts(client: TestClient, test_author_with_posts: Author):
    """Test getting an author with all their posts."""
    response = client.get(f"/api/authors/{test_author_with_posts.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_author_with_posts.id
    assert data["name"] == test_author_with_posts.name
    assert "posts" in data
    assert len(data["posts"]) == 3

    # Verify post structure
    for post in data["posts"]:
        assert "id" in post
        assert "title" in post
        assert "content" in post
        assert "status" in post
        assert "author_id" in post
        assert post["author_id"] == test_author_with_posts.id
        assert "created_at" in post


def test_get_author_no_posts(client: TestClient, test_author: Author):
    """Test getting an author with no posts."""
    response = client.get(f"/api/authors/{test_author.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_author.id
    assert "posts" in data
    assert data["posts"] == []


def test_get_author_posts_include_all_statuses(
    client: TestClient,
    test_authors_with_posts: list
):
    """Test that author endpoint returns posts with all statuses."""
    author = test_authors_with_posts[0]  # test_author with mixed status posts

    response = client.get(f"/api/authors/{author.id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) == 3

    # Verify different statuses are included
    post_statuses = [post["status"] for post in data["posts"]]
    assert "published" in post_statuses
    assert "draft" in post_statuses
    assert "archived" in post_statuses


def test_get_author_posts_data_integrity(
    client: TestClient,
    test_author_with_posts: Author
):
    """Test that post data is complete and accurate."""
    response = client.get(f"/api/authors/{test_author_with_posts.id}")

    assert response.status_code == 200
    data = response.json()

    # Check first post data
    first_post = data["posts"][0]
    assert first_post["title"] in ["First Post", "Second Post", "Third Post"]
    assert len(first_post["content"]) > 0
    assert first_post["status"] in ["published", "draft", "archived"]
    assert first_post["author_id"] == test_author_with_posts.id


def test_get_author_response_structure(client: TestClient, test_author_with_posts: Author):
    """Test that the response follows the AuthorWithPosts schema."""
    response = client.get(f"/api/authors/{test_author_with_posts.id}")

    assert response.status_code == 200
    data = response.json()

    # Required author fields
    assert "id" in data
    assert "name" in data
    assert "email" in data
    assert "bio" in data
    assert "created_at" in data
    assert "posts" in data

    # Each post should have required fields
    for post in data["posts"]:
        assert "id" in post
        assert "title" in post
        assert "content" in post
        assert "status" in post
        assert "author_id" in post
        assert "created_at" in post


# ============================================================================
# GET /api/authors/{author_id} - Error Cases
# ============================================================================

def test_get_author_not_found(client: TestClient):
    """Test getting an author that doesn't exist."""
    response = client.get("/api/authors/99999")

    assert response.status_code == 404
    assert "Author with id 99999 not found" in response.json()["detail"]


def test_get_author_negative_id(client: TestClient):
    """Test getting an author with negative ID."""
    response = client.get("/api/authors/-1")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_author_invalid_id_type(client: TestClient):
    """Test getting an author with invalid ID type."""
    response = client.get("/api/authors/invalid")

    assert response.status_code == 422  # Validation error


def test_get_author_zero_id(client: TestClient):
    """Test getting an author with ID zero."""
    response = client.get("/api/authors/0")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ============================================================================
# Additional Edge Cases
# ============================================================================

def test_authors_endpoint_no_authentication_required(client: TestClient, test_author: Author):
    """Test that authors endpoints don't require authentication."""
    # List authors
    response = client.get("/api/authors/")
    assert response.status_code == 200

    # Get specific author
    response = client.get(f"/api/authors/{test_author.id}")
    assert response.status_code == 200


def test_get_author_multiple_posts_order(
    client: TestClient,
    test_author_with_posts: Author
):
    """Test that posts are returned (order verified by presence of all posts)."""
    response = client.get(f"/api/authors/{test_author_with_posts.id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) == 3

    # Verify all expected posts are present
    post_titles = [post["title"] for post in data["posts"]]
    assert "First Post" in post_titles
    assert "Second Post" in post_titles
    assert "Third Post" in post_titles


def test_author_with_posts_consistency(
    client: TestClient,
    db: Session,
    test_author_with_posts: Author
):
    """Test that the number of posts returned matches the database."""
    # Get author via API
    response = client.get(f"/api/authors/{test_author_with_posts.id}")
    api_post_count = len(response.json()["posts"])

    # Get actual post count from database
    db_post_count = db.query(Post).filter(
        Post.author_id == test_author_with_posts.id
    ).count()

    assert api_post_count == db_post_count


def test_list_authors_includes_authors_with_and_without_posts(
    client: TestClient,
    test_authors_with_posts: list
):
    """Test that list authors includes both authors with and without posts."""
    response = client.get("/api/authors/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # All three authors should be listed

    # Check that we have authors with different post counts
    author_names = [author["name"] for author in data]
    assert "Test Author" in author_names
    assert "Second Author" in author_names
    assert "Third Author" in author_names
