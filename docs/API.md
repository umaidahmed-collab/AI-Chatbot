# API Documentation

## Overview

The AI Chatbot API is built with FastAPI and provides endpoints for user authentication, chat functionality, and document management.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "full_name": "string" // optional
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "full_name": "string",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Login
```http
POST /api/auth/token
```

**Request Body (form-data):**
```
username: string
password: string
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/auth/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "full_name": "string",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Chat

#### Send Message
```http
POST /api/chat/
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "message": "string",
  "session_id": 1, // optional
  "use_documents": true
}
```

**Response:**
```json
{
  "message": "AI response",
  "session_id": 1,
  "sources": ["Document 1", "Document 2"] // optional
}
```

#### Get Chat Sessions
```http
GET /api/chat/sessions
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Chat Session",
    "user_id": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "messages": []
  }
]
```

#### Get Session Messages
```http
GET /api/chat/sessions/{session_id}/messages
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "session_id": 1,
    "content": "Hello",
    "role": "user",
    "timestamp": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "session_id": 1,
    "content": "Hi there!",
    "role": "assistant",
    "timestamp": "2024-01-01T00:00:00Z"
  }
]
```

#### Create Chat Session
```http
POST /api/chat/sessions?title=New Chat
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "title": "New Chat",
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "messages": []
}
```

### Documents

#### Upload Document
```http
POST /api/documents/upload
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
```
file: <file> // PDF, DOCX, or TXT file
```

**Response:**
```json
{
  "id": 1,
  "filename": "unique_filename.pdf",
  "original_filename": "document.pdf",
  "file_path": "/path/to/file",
  "file_size": 1024,
  "content_type": "application/pdf",
  "processed": false,
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Get Documents
```http
GET /api/documents/
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "filename": "unique_filename.pdf",
    "original_filename": "document.pdf",
    "file_path": "/path/to/file",
    "file_size": 1024,
    "content_type": "application/pdf",
    "processed": true,
    "owner_id": 1,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Delete Document
```http
DELETE /api/documents/{document_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 100 requests per minute per IP address
- 1000 requests per hour per authenticated user

## File Upload Limits

- Maximum file size: 10MB
- Supported formats: PDF, DOCX, TXT
- Maximum files per user: 100

## WebSocket

### Real-time Chat
```
ws://localhost:8000/api/chat/ws/{session_id}
```

Send and receive messages in real-time format:

**Send:**
```json
{
  "message": "Hello",
  "use_documents": true
}
```

**Receive:**
```json
{
  "message": "AI response",
  "timestamp": "2024-01-01T00:00:00Z"
}
```
