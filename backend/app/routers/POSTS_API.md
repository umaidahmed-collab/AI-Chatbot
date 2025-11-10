# Posts API Documentation

## Overview

The Posts API provides comprehensive CRUD operations for managing blog posts. All endpoints follow RESTful conventions and include proper validation, error handling, and authorization.

**Base Path:** `/api/posts`

**Authentication:** Most endpoints require JWT authentication via Bearer token (except GET endpoints which are public).

---

## Data Models

### Post Schema

```json
{
  "id": 1,
  "author_id": 1,
  "title": "My Blog Post",
  "content": "Post content here...",
  "status": "draft",
  "created_at": "2025-11-10T12:00:00Z",
  "updated_at": "2025-11-10T12:30:00Z",
  "author": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "Author biography",
    "created_at": "2025-11-10T10:00:00Z"
  }
}
```

### Post Status Enum

- `draft` - Post is in draft state, not published
- `published` - Post is publicly available
- `archived` - Post is archived and not visible

---

## Endpoints

### 1. Create Post

**POST** `/api/posts/`

Creates a new blog post with validation.

#### Authentication
- **Required:** Yes (Bearer token)
- **Access:** Authenticated users

#### Request Body

```json
{
  "author_id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my blog post.",
  "status": "draft"  // Optional, defaults to "draft"
}
```

#### Validation Rules
- `author_id`: Required, must exist in database
- `title`: Required, 1-255 characters
- `content`: Required, minimum 1 character
- `status`: Optional, must be one of: draft, published, archived

#### Response

**Status Code:** `201 Created`

```json
{
  "id": 1,
  "author_id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my blog post.",
  "status": "draft",
  "created_at": "2025-11-10T12:00:00Z",
  "updated_at": null,
  "author": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "Author biography",
    "created_at": "2025-11-10T10:00:00Z"
  }
}
```

#### Error Responses

**400 Bad Request** - Invalid author_id
```json
{
  "detail": "Author with id 999 not found"
}
```

**401 Unauthorized** - Missing or invalid authentication
```json
{
  "detail": "Could not validate credentials"
}
```

**422 Unprocessable Entity** - Validation error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/posts/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "author_id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my blog post.",
    "status": "draft"
  }'
```

---

### 2. List Posts

**GET** `/api/posts/`

Retrieves a paginated list of posts with optional filtering.

#### Authentication
- **Required:** No (Public endpoint)

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `skip` | integer | No | 0 | Number of records to skip (for pagination) |
| `limit` | integer | No | 10 | Maximum records to return (1-100) |
| `status` | string | No | - | Filter by status (draft/published/archived) |
| `author_id` | integer | No | - | Filter by author ID |

#### Response

**Status Code:** `200 OK`

```json
{
  "total": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3,
  "items": [
    {
      "id": 1,
      "author_id": 1,
      "title": "My First Blog Post",
      "content": "Post content...",
      "status": "published",
      "created_at": "2025-11-10T12:00:00Z",
      "updated_at": "2025-11-10T12:30:00Z",
      "author": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "bio": "Author biography",
        "created_at": "2025-11-10T10:00:00Z"
      }
    }
  ]
}
```

#### Example Requests

```bash
# Basic pagination
curl "http://localhost:8000/api/posts/?skip=0&limit=10"

# Filter by status
curl "http://localhost:8000/api/posts/?status=published"

# Filter by author
curl "http://localhost:8000/api/posts/?author_id=1"

# Combined filters and pagination
curl "http://localhost:8000/api/posts/?skip=10&limit=20&status=published&author_id=1"
```

#### Notes
- Posts are returned in descending order by `created_at` (newest first)
- The `page` field is calculated as: `(skip / limit) + 1`
- The `total_pages` field is calculated as: `ceil(total / limit)`

---

### 3. Get Post by ID

**GET** `/api/posts/{post_id}`

Retrieves a single post by its ID.

#### Authentication
- **Required:** No (Public endpoint)

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `post_id` | integer | ID of the post to retrieve |

#### Response

**Status Code:** `200 OK`

```json
{
  "id": 1,
  "author_id": 1,
  "title": "My First Blog Post",
  "content": "Post content...",
  "status": "published",
  "created_at": "2025-11-10T12:00:00Z",
  "updated_at": "2025-11-10T12:30:00Z",
  "author": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "Author biography",
    "created_at": "2025-11-10T10:00:00Z"
  }
}
```

#### Error Responses

**404 Not Found** - Post does not exist
```json
{
  "detail": "Post with id 999 not found"
}
```

#### Example Request

```bash
curl "http://localhost:8000/api/posts/1"
```

---

### 4. Update Post

**PUT** `/api/posts/{post_id}`

Updates an existing post. Only provided fields are updated.

#### Authentication
- **Required:** Yes (Bearer token)
- **Access:** Authenticated users

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `post_id` | integer | ID of the post to update |

#### Request Body

All fields are optional. Only provided fields will be updated.

```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "status": "published",
  "author_id": 2
}
```

#### Validation Rules
- `title`: If provided, 1-255 characters
- `content`: If provided, minimum 1 character
- `status`: If provided, must be: draft, published, or archived
- `author_id`: If provided, must exist in database

#### Response

**Status Code:** `200 OK`

```json
{
  "id": 1,
  "author_id": 2,
  "title": "Updated Title",
  "content": "Updated content...",
  "status": "published",
  "created_at": "2025-11-10T12:00:00Z",
  "updated_at": "2025-11-10T13:00:00Z",
  "author": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "bio": "Another author",
    "created_at": "2025-11-10T11:00:00Z"
  }
}
```

#### Error Responses

**404 Not Found** - Post does not exist
```json
{
  "detail": "Post with id 999 not found"
}
```

**400 Bad Request** - Invalid author_id
```json
{
  "detail": "Author with id 999 not found"
}
```

**401 Unauthorized** - Missing or invalid authentication
```json
{
  "detail": "Could not validate credentials"
}
```

#### Example Requests

```bash
# Update title and status
curl -X PUT "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "status": "published"
  }'

# Update only content
curl -X PUT "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "New content for this post"
  }'
```

---

### 5. Delete Post

**DELETE** `/api/posts/{post_id}`

Permanently deletes a post. This operation cannot be undone.

#### Authentication
- **Required:** Yes (Bearer token)
- **Access:** Authenticated users

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `post_id` | integer | ID of the post to delete |

#### Response

**Status Code:** `204 No Content`

No response body.

#### Error Responses

**404 Not Found** - Post does not exist
```json
{
  "detail": "Post with id 999 not found"
}
```

**401 Unauthorized** - Missing or invalid authentication
```json
{
  "detail": "Could not validate credentials"
}
```

#### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer <token>"
```

---

## Implementation Details

### File Location
`backend/app/routers/posts.py`

### Dependencies
- **Database:** SQLAlchemy ORM with PostgreSQL
- **Schemas:** Pydantic models in `app.models.schemas`
- **Models:** SQLAlchemy models in `app.models.database`
- **Authentication:** JWT tokens via `app.services.auth`

### Database Relationships
- Post belongs to Author (many-to-one)
- Author relationship is automatically loaded with posts

### Security Features
- JWT authentication on write operations (POST, PUT, DELETE)
- Input validation using Pydantic schemas
- SQL injection protection via SQLAlchemy ORM
- Foreign key validation for author_id

### Performance Considerations
- Pagination prevents loading large datasets
- Database indexes on `id`, `author_id`, and `status` fields
- Efficient query filtering with SQLAlchemy
- Descending order by `created_at` for chronological listing

---

## Testing

### Manual Testing with curl

1. **Get authentication token:**
```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass"
```

2. **Create a post:**
```bash
curl -X POST "http://localhost:8000/api/posts/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "author_id": 1,
    "title": "Test Post",
    "content": "Test content"
  }'
```

3. **List posts:**
```bash
curl "http://localhost:8000/api/posts/"
```

4. **Get specific post:**
```bash
curl "http://localhost:8000/api/posts/1"
```

5. **Update post:**
```bash
curl -X PUT "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "published"}'
```

6. **Delete post:**
```bash
curl -X DELETE "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer <token>"
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Both interfaces allow testing all endpoints directly from the browser.

---

## Integration with Main Application

The posts router is registered in `backend/app/main.py`:

```python
from app.routers import posts

app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
```

This makes all endpoints available under the `/api/posts` prefix with the "posts" tag for documentation grouping.

---

## Error Handling Summary

| Status Code | Scenario |
|-------------|----------|
| 200 | Successful GET or PUT request |
| 201 | Successful POST (create) request |
| 204 | Successful DELETE request |
| 400 | Invalid input (e.g., non-existent author_id) |
| 401 | Missing or invalid authentication |
| 404 | Resource not found |
| 422 | Validation error (invalid request body) |

All error responses include a `detail` field with a descriptive message.
