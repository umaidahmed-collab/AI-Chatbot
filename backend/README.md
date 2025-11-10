# AI Chatbot Backend API

A FastAPI-based backend service for an AI-powered chatbot with document upload, vector embeddings, and Retrieval-Augmented Generation (RAG) capabilities.

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Authentication and Authorization](#authentication-and-authorization)
- [Document Processing Pipeline](#document-processing-pipeline)
- [Chat Service and RAG Integration](#chat-service-and-rag-integration)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Code Structure](#code-structure)
- [Dependencies](#dependencies)
- [Development Workflow](#development-workflow)
- [Contributing](#contributing)

## Project Overview

This backend provides a complete REST API for an AI chatbot application that enables:

- **User Authentication**: Secure registration and JWT-based authentication
- **Document Management**: Upload and process PDF, DOCX, and TXT files
- **Vector Embeddings**: Automatic text extraction, chunking, and embedding generation
- **RAG Integration**: Context-aware responses using relevant document chunks
- **Real-time Chat**: WebSocket support for live conversations
- **Persistent Storage**: PostgreSQL for structured data, ChromaDB for vector embeddings

The system uses Retrieval-Augmented Generation (RAG) to provide AI responses grounded in uploaded documents, combining the power of Large Language Models with user-specific knowledge bases.

## Technology Stack

### Core Framework
- **FastAPI** (0.108.0): Modern, high-performance web framework with automatic API documentation
- **Uvicorn** (0.25.0): ASGI server with hot-reload for development

### Database & ORM
- **PostgreSQL**: Primary relational database
- **SQLAlchemy** (2.0.25): SQL toolkit and ORM
- **Alembic** (1.13.1): Database migration tool
- **ChromaDB** (0.4.22): Vector database for embeddings

### Authentication & Security
- **python-jose[cryptography]** (3.3.0): JWT token generation and validation
- **passlib[bcrypt]** (1.7.4): Password hashing with bcrypt

### AI & Machine Learning
- **OpenAI GPT-3.5-turbo**: Language model for chat responses
- **LangChain** (0.1.0): Framework for LLM applications
- **sentence-transformers** (2.2.2): Text embedding generation (all-MiniLM-L6-v2)

### Document Processing
- **PyPDF2** (3.0.1): PDF text extraction
- **python-docx** (1.1.0): DOCX text extraction
- **RecursiveCharacterTextSplitter**: Intelligent text chunking with overlap

### Additional Services
- **Redis** (5.0.1): Caching and session management
- **WebSockets**: Real-time communication
- **aiofiles** (23.2.0): Async file I/O operations

## Architecture

### Layered Architecture Pattern

The backend follows a clean, layered architecture that separates concerns and improves maintainability:

```
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (Routers)                     │
│  - HTTP request handling                                    │
│  - Request validation (Pydantic)                           │
│  - Response serialization                                   │
│  - Dependency injection                                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer (Services)           │
│  - Authentication logic                                     │
│  - Document processing orchestration                        │
│  - Chat service with RAG integration                        │
│  - Database operations                                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer (Models)                      │
│  - SQLAlchemy ORM models                                    │
│  - Pydantic schemas                                         │
│  - Database relationships                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                       │
│  - PostgreSQL (structured data)                             │
│  - ChromaDB (vector embeddings)                            │
│  - Redis (caching)                                          │
│  - File system (uploads)                                    │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Patterns

#### 1. Dependency Injection

FastAPI's dependency injection system is used throughout for:

- **Database sessions**: `get_db()` provides a database session per request
- **Authentication**: `get_current_user()` validates JWT tokens
- **Authorization**: `get_current_active_user()` ensures active user status

Example:
```python
@router.get("/documents")
async def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Automatically injected dependencies
    return document_service.get_user_documents(db, current_user.id)
```

#### 2. Service Layer Pattern

All business logic is encapsulated in service classes:

- **AuthService**: Password hashing, token generation, user verification
- **DocumentProcessor**: File handling, text extraction, embedding generation
- **ChatService**: Conversation management, RAG integration, OpenAI communication
- **DatabaseService**: Connection management, session handling

This pattern:
- Isolates business logic from HTTP layer
- Enables easier testing with mocks
- Promotes code reusability
- Simplifies maintenance

#### 3. RAG (Retrieval-Augmented Generation) Pipeline

The RAG pipeline enhances AI responses with relevant document context:

```
User Query
    ↓
Generate Query Embedding (HuggingFace)
    ↓
Vector Similarity Search (ChromaDB)
    ↓
Retrieve Top 5 Most Similar Chunks
    ↓
Inject Context into System Prompt
    ↓
Add Conversation History (Last 10 Messages)
    ↓
Call OpenAI GPT-3.5-turbo
    ↓
Return AI Response with Source Citations
```

#### 4. Async/Await Pattern

Async operations for I/O-bound tasks:

- File uploads and downloads
- Database queries (where applicable)
- External API calls (OpenAI)
- WebSocket connections

## Prerequisites

Before setting up the backend, ensure you have:

### Required Software

- **Python**: 3.9 or higher
- **PostgreSQL**: 12 or higher
- **Redis**: 6 or higher (for caching)
- **pip**: Python package manager

### Optional

- **Docker & Docker Compose**: For containerized deployment
- **Git**: For version control
- **Virtual environment tool**: venv, virtualenv, or conda

### External Services

- **OpenAI API Key**: Required for AI-powered responses (optional with fallback)
  - Sign up at: https://platform.openai.com/
  - Get API key from: https://platform.openai.com/api-keys

## Setup and Installation

### Option 1: Local Development Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Chatbot/backend
```

#### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up PostgreSQL Database

```bash
# Create database
psql -U postgres
CREATE DATABASE chatbot_db;
CREATE USER chatbot WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot;
\q
```

#### 5. Start Redis

```bash
# Using Homebrew on macOS
brew services start redis

# Using Docker
docker run -d -p 6379:6379 redis:latest

# Using apt on Linux
sudo systemctl start redis
```

#### 6. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
# Edit .env with your configuration (see Configuration section)
```

#### 7. Initialize the Application

```bash
# The application will automatically create:
# - Database tables (via SQLAlchemy)
# - Upload directory (uploads/)
# - ChromaDB directory (chroma_db/)
```

#### 8. Run the Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Option 2: Docker Development Setup

#### 1. Build and Start Containers

```bash
# From project root
cd AI-Chatbot

# Development setup with hot-reload
docker-compose -f docker-compose.dev.yml up --build

# Production setup
docker-compose up --build
```

#### 2. Access the Application

- **API**: http://localhost:8000
- **Postgres**: localhost:5432
- **Redis**: localhost:6379

#### 3. View Logs

```bash
docker-compose logs -f backend
```

#### 4. Stop Containers

```bash
docker-compose down

# Remove volumes (clears database)
docker-compose down -v
```

### Verify Installation

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-10T..."
}
```

## Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

#### Database Configuration

```bash
# PostgreSQL connection string
DATABASE_URL=postgresql://chatbot:password@localhost:5432/chatbot_db

# For Docker setup
# DATABASE_URL=postgresql://chatbot:password@postgres:5432/chatbot_db
```

#### Security Configuration

```bash
# Secret key for JWT signing (CHANGE IN PRODUCTION!)
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32

# JWT algorithm
ALGORITHM=HS256

# Token expiration in minutes
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Generate a secure secret key:**
```bash
openssl rand -hex 32
```

#### External Services

```bash
# OpenAI API Key (optional - has fallback)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Redis connection string
REDIS_URL=redis://localhost:6379

# For Docker setup
# REDIS_URL=redis://redis:6379
```

#### CORS Configuration

```bash
# Comma-separated list of allowed origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

#### File Upload Configuration

```bash
# Directory for storing uploaded files
UPLOAD_DIR=uploads

# Maximum file size in bytes (10MB)
MAX_FILE_SIZE=10485760

# Allowed file extensions (comma-separated)
ALLOWED_FILE_TYPES=.pdf,.txt,.docx
```

#### Vector Database Configuration

```bash
# ChromaDB persistent storage directory
CHROMA_DB_PATH=chroma_db
```

#### Application Settings

```bash
# Environment mode
ENVIRONMENT=development

# Debug mode (disable in production)
DEBUG=true
```

### Configuration Loading

Configuration is managed by `app/utils/config.py` using Pydantic's `BaseSettings`:

```python
from app.utils.config import settings

# Access configuration values
database_url = settings.DATABASE_URL
secret_key = settings.SECRET_KEY
max_file_size = settings.MAX_FILE_SIZE
```

Benefits:
- **Type validation**: Pydantic ensures correct types
- **Environment variable support**: Automatic `.env` loading
- **Default values**: Fallbacks for optional settings
- **Immutable**: Settings cannot be changed at runtime

## Database Schema

### Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────┐
│                            User                              │
├─────────────────────────────────────────────────────────────┤
│ PK  id: Integer                                              │
│ UQ  username: String(50)                                     │
│ UQ  email: String(100)                                       │
│     hashed_password: String(255)                             │
│     full_name: String(100)                                   │
│     is_active: Boolean                                       │
│     created_at: DateTime                                     │
│     updated_at: DateTime                                     │
└─────────────────────────────────────────────────────────────┘
           │                           │
           │ 1:M                       │ 1:M
           ↓                           ↓
┌──────────────────────────┐  ┌──────────────────────────┐
│        Document          │  │      ChatSession         │
├──────────────────────────┤  ├──────────────────────────┤
│ PK  id: Integer          │  │ PK  id: Integer          │
│     filename: String     │  │     title: String(255)   │
│     original_filename    │  │ FK  user_id: Integer     │
│     file_path: String    │  │     created_at: DateTime │
│     file_size: Integer   │  │     updated_at: DateTime │
│     content_type: String │  └──────────────────────────┘
│     processed: Boolean   │             │
│ FK  owner_id: Integer    │             │ 1:M
│     created_at: DateTime │             ↓
│     updated_at: DateTime │  ┌──────────────────────────┐
└──────────────────────────┘  │      ChatMessage         │
                              ├──────────────────────────┤
                              │ PK  id: Integer          │
                              │ FK  session_id: Integer  │
                              │     content: Text        │
                              │     role: String(20)     │
                              │     timestamp: DateTime  │
                              └──────────────────────────┘
```

### Table Definitions

#### User Table

**Purpose**: Stores user accounts and authentication information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing user identifier |
| username | String(50) | UNIQUE, NOT NULL, INDEXED | Unique username for login |
| email | String(100) | UNIQUE, NOT NULL, INDEXED | User's email address |
| hashed_password | String(255) | NOT NULL | Bcrypt-hashed password |
| full_name | String(100) | NULLABLE | User's display name |
| is_active | Boolean | DEFAULT true | Account active status |
| created_at | DateTime | DEFAULT now() | Account creation timestamp |
| updated_at | DateTime | ON UPDATE now() | Last modification timestamp |

**Relationships**:
- One-to-many with `Document` (user can own multiple documents)
- One-to-many with `ChatSession` (user can have multiple chat sessions)

**Indexes**:
- `ix_users_username` on `username`
- `ix_users_email` on `email`

#### Document Table

**Purpose**: Tracks uploaded documents and processing status

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing document identifier |
| filename | String(255) | NOT NULL | System-generated unique filename (UUID) |
| original_filename | String(255) | NOT NULL | Original uploaded filename |
| file_path | String(500) | NOT NULL | Full path to file on disk |
| file_size | Integer | NOT NULL | File size in bytes |
| content_type | String(100) | NOT NULL | MIME type (application/pdf, etc.) |
| processed | Boolean | DEFAULT false | Processing status flag |
| owner_id | Integer | FOREIGN KEY → User.id | Document owner |
| created_at | DateTime | DEFAULT now() | Upload timestamp |
| updated_at | DateTime | ON UPDATE now() | Last modification timestamp |

**Relationships**:
- Many-to-one with `User` (document belongs to one user)

**Cascade Rules**:
- ON DELETE CASCADE: Deleting a user deletes their documents

#### ChatSession Table

**Purpose**: Groups related chat messages into conversations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing session identifier |
| title | String(255) | DEFAULT "New Chat" | Session title/name |
| user_id | Integer | FOREIGN KEY → User.id | Session owner |
| created_at | DateTime | DEFAULT now() | Session creation timestamp |
| updated_at | DateTime | ON UPDATE now() | Last activity timestamp |

**Relationships**:
- Many-to-one with `User` (session belongs to one user)
- One-to-many with `ChatMessage` (session contains multiple messages)

**Cascade Rules**:
- ON DELETE CASCADE: Deleting a user deletes their sessions
- ON DELETE CASCADE: Deleting a session deletes its messages

#### ChatMessage Table

**Purpose**: Stores individual messages within chat sessions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing message identifier |
| session_id | Integer | FOREIGN KEY → ChatSession.id | Parent session |
| content | Text | NOT NULL | Message text content |
| role | String(20) | NOT NULL | "user" or "assistant" |
| timestamp | DateTime | DEFAULT now() | Message creation timestamp |

**Relationships**:
- Many-to-one with `ChatSession` (message belongs to one session)

**Cascade Rules**:
- ON DELETE CASCADE: Deleting a session deletes its messages

### Vector Database Schema (ChromaDB)

**Collection Name**: `documents`

**Structure**:
- **Documents**: Text chunks from uploaded files
- **Embeddings**: 384-dimensional vectors (all-MiniLM-L6-v2)
- **Metadata**: JSON objects containing:
  - `document_id`: Integer (references Document.id)
  - `chunk_index`: Integer (position in original document)
  - `file_path`: String (full path to source file)
- **IDs**: UUID-based unique identifiers per chunk

**Distance Metric**: Cosine similarity

**Example Query**:
```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)
```

## API Endpoints

### Authentication Router (`/api/auth`)

**Base Path**: `/api/auth`

#### 1. Register New User

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-11-10T10:00:00Z",
  "updated_at": "2025-11-10T10:00:00Z"
}
```

**Errors**:
- 400: Username or email already exists
- 422: Validation error (invalid email format, weak password, etc.)

---

#### 2. Login (Get Token)

```http
POST /api/auth/token
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=SecurePass123!
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**:
- 401: Incorrect username or password
- 422: Missing or invalid form data

**Usage**: Include token in Authorization header for protected routes:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

#### 3. Get Current User

```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-11-10T10:00:00Z",
  "updated_at": "2025-11-10T10:00:00Z"
}
```

**Errors**:
- 401: Missing, invalid, or expired token

---

### Users Router (`/api/users`)

**Base Path**: `/api/users`

#### 1. List All Users

```http
GET /api/users?skip=0&limit=10
Authorization: Bearer <token>
```

**Query Parameters**:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 10, max: 100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2025-11-10T10:00:00Z",
    "updated_at": "2025-11-10T10:00:00Z"
  },
  {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "full_name": "Jane Doe",
    "is_active": true,
    "created_at": "2025-11-10T11:00:00Z",
    "updated_at": "2025-11-10T11:00:00Z"
  }
]
```

---

#### 2. Get Specific User

```http
GET /api/users/1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-11-10T10:00:00Z",
  "updated_at": "2025-11-10T10:00:00Z"
}
```

**Errors**:
- 404: User not found

---

#### 3. Update User

```http
PUT /api/users/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Smith",
  "password": "NewSecurePass456!"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Smith",
  "is_active": true,
  "created_at": "2025-11-10T10:00:00Z",
  "updated_at": "2025-11-10T15:30:00Z"
}
```

**Errors**:
- 403: Permission denied (can only update own profile)
- 404: User not found

**Note**: All fields are optional. Password will be hashed if provided.

---

### Documents Router (`/api/documents`)

**Base Path**: `/api/documents`

#### 1. Upload Document

```http
POST /api/documents/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file=@document.pdf
```

**Response** (200 OK):
```json
{
  "id": 1,
  "filename": "a7f3e8b2-4c5d-6e7f-8a9b-0c1d2e3f4g5h.pdf",
  "original_filename": "document.pdf",
  "file_path": "/uploads/a7f3e8b2-4c5d-6e7f-8a9b-0c1d2e3f4g5h.pdf",
  "file_size": 2048576,
  "content_type": "application/pdf",
  "processed": false,
  "owner_id": 1,
  "created_at": "2025-11-10T12:00:00Z",
  "updated_at": "2025-11-10T12:00:00Z"
}
```

**Processing**:
- File saved immediately
- Background task processes document asynchronously
- `processed` flag updates to `true` when complete
- Check status with GET endpoint

**Errors**:
- 400: File type not allowed or file too large
- 413: Request entity too large
- 422: No file provided

**Supported Formats**:
- PDF (`.pdf`) - up to 10MB
- DOCX (`.docx`) - up to 10MB
- TXT (`.txt`) - up to 10MB

---

#### 2. List User's Documents

```http
GET /api/documents
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "filename": "a7f3e8b2-4c5d-6e7f-8a9b-0c1d2e3f4g5h.pdf",
    "original_filename": "document.pdf",
    "file_path": "/uploads/a7f3e8b2-4c5d-6e7f-8a9b-0c1d2e3f4g5h.pdf",
    "file_size": 2048576,
    "content_type": "application/pdf",
    "processed": true,
    "owner_id": 1,
    "created_at": "2025-11-10T12:00:00Z",
    "updated_at": "2025-11-10T12:05:00Z"
  }
]
```

---

#### 3. Get Specific Document

```http
GET /api/documents/1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "filename": "a7f3e8b2-4c5d-6e7f-8a9b-0c1d2e3f4g5h.pdf",
  "original_filename": "document.pdf",
  "file_path": "/uploads/a7f3e8b2-4c5d-6e7f-8a9b-0c1d2e3f4g5h.pdf",
  "file_size": 2048576,
  "content_type": "application/pdf",
  "processed": true,
  "owner_id": 1,
  "created_at": "2025-11-10T12:00:00Z",
  "updated_at": "2025-11-10T12:05:00Z"
}
```

**Errors**:
- 403: Permission denied (not document owner)
- 404: Document not found

---

#### 4. Delete Document

```http
DELETE /api/documents/1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "message": "Document deleted successfully"
}
```

**Actions**:
- Deletes file from disk
- Removes database record
- Removes vector embeddings from ChromaDB

**Errors**:
- 403: Permission denied (not document owner)
- 404: Document not found

---

### Chat Router (`/api/chat`)

**Base Path**: `/api/chat`

#### 1. Send Chat Message

```http
POST /api/chat/
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "What are the main topics in my uploaded documents?",
  "session_id": 1,
  "use_documents": true
}
```

**Request Fields**:
- `message` (required): User's message text
- `session_id` (optional): Existing session ID (creates new if omitted)
- `use_documents` (optional): Enable RAG with document context (default: false)

**Response** (200 OK):
```json
{
  "message": "Based on your uploaded documents, the main topics include machine learning fundamentals, neural network architectures, and training optimization techniques.",
  "session_id": 1,
  "sources": [1, 2]
}
```

**Response Fields**:
- `message`: AI-generated response
- `session_id`: Session ID (for follow-up messages)
- `sources`: List of document IDs used (only if `use_documents=true`)

**Errors**:
- 404: Session not found or not owned by user
- 500: OpenAI API error (returns fallback response)

---

#### 2. Get User's Chat Sessions

```http
GET /api/chat/sessions
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Document Analysis",
    "user_id": 1,
    "created_at": "2025-11-10T13:00:00Z",
    "updated_at": "2025-11-10T13:15:00Z",
    "messages": []
  },
  {
    "id": 2,
    "title": "New Chat",
    "user_id": 1,
    "created_at": "2025-11-10T14:00:00Z",
    "updated_at": "2025-11-10T14:00:00Z",
    "messages": []
  }
]
```

---

#### 3. Get Specific Session

```http
GET /api/chat/sessions/1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Document Analysis",
  "user_id": 1,
  "created_at": "2025-11-10T13:00:00Z",
  "updated_at": "2025-11-10T13:15:00Z",
  "messages": [
    {
      "id": 1,
      "session_id": 1,
      "content": "What are the main topics?",
      "role": "user",
      "timestamp": "2025-11-10T13:00:00Z"
    },
    {
      "id": 2,
      "session_id": 1,
      "content": "The main topics include...",
      "role": "assistant",
      "timestamp": "2025-11-10T13:00:05Z"
    }
  ]
}
```

**Errors**:
- 403: Permission denied (not session owner)
- 404: Session not found

---

#### 4. Get Session Messages

```http
GET /api/chat/sessions/1/messages
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "session_id": 1,
    "content": "What are the main topics?",
    "role": "user",
    "timestamp": "2025-11-10T13:00:00Z"
  },
  {
    "id": 2,
    "session_id": 1,
    "content": "The main topics include...",
    "role": "assistant",
    "timestamp": "2025-11-10T13:00:05Z"
  }
]
```

---

#### 5. Create New Session

```http
POST /api/chat/sessions?title=My%20New%20Chat
Authorization: Bearer <token>
```

**Query Parameters**:
- `title` (optional): Session title (default: "New Chat")

**Response** (200 OK):
```json
{
  "id": 3,
  "title": "My New Chat",
  "user_id": 1,
  "created_at": "2025-11-10T15:00:00Z",
  "updated_at": "2025-11-10T15:00:00Z",
  "messages": []
}
```

---

#### 6. WebSocket Chat (Real-time)

```javascript
// JavaScript example
const ws = new WebSocket('ws://localhost:8000/api/chat/ws/1?token=<jwt_token>');

ws.onopen = () => {
  ws.send(JSON.stringify({
    message: "Hello!",
    use_documents: true
  }));
};

ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log('AI:', response.message);
};
```

**Connection URL**: `ws://localhost:8000/api/chat/ws/{session_id}?token=<jwt_token>`

**Message Format** (Client → Server):
```json
{
  "message": "Your message here",
  "use_documents": true
}
```

**Message Format** (Server → Client):
```json
{
  "message": "AI response here",
  "session_id": 1,
  "sources": [1, 2]
}
```

---

### Health & Status Endpoints

#### Health Check

```http
GET /health
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-11-10T15:30:00Z"
}
```

---

#### Root Endpoint

```http
GET /
```

**Response** (200 OK):
```json
{
  "message": "AI Chatbot API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### Interactive API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Explore all endpoints
- Test requests with authentication
- View request/response schemas
- See detailed parameter descriptions

## Authentication and Authorization

### JWT-Based Authentication

The backend uses **JSON Web Tokens (JWT)** for stateless authentication.

### Authentication Flow

```
┌──────────┐                                   ┌──────────┐
│  Client  │                                   │  Server  │
└──────────┘                                   └──────────┘
     │                                                │
     │  1. POST /api/auth/register                   │
     │  (username, email, password)                  │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                    2. Hash password (bcrypt)  │
     │                    3. Store user in DB        │
     │                                                │
     │  4. Return user object                        │
     │<───────────────────────────────────────────────┤
     │                                                │
     │  5. POST /api/auth/token                      │
     │  (username, password)                         │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                    6. Verify password         │
     │                    7. Generate JWT token      │
     │                                                │
     │  8. Return access_token                       │
     │<───────────────────────────────────────────────┤
     │                                                │
     │  9. Store token in memory/localStorage        │
     │                                                │
     │  10. Protected request                        │
     │  Authorization: Bearer <token>                │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                    11. Verify JWT signature   │
     │                    12. Decode payload         │
     │                    13. Get user from DB       │
     │                    14. Check is_active        │
     │                                                │
     │  15. Return protected resource                │
     │<───────────────────────────────────────────────┤
     │                                                │
```

### Password Security

**Hashing Algorithm**: bcrypt with salt

**Implementation** (`app/services/auth.py`):
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
```

**Benefits**:
- Adaptive cost factor (slows down brute-force attacks)
- Built-in salt generation (prevents rainbow table attacks)
- Industry-standard security

### JWT Token Structure

**Token Payload**:
```json
{
  "sub": "johndoe",
  "exp": 1699632000
}
```

**Fields**:
- `sub` (subject): Username
- `exp` (expiration): Unix timestamp (30 minutes from issue)

**Token Generation** (`app/services/auth.py`):
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils.config import settings

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Generate a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
```

**Token Validation**:
```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Validate JWT token and return current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user
```

### Authorization Patterns

#### 1. Route-Level Protection

```python
from fastapi import Depends
from app.services.auth import get_current_active_user

@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_active_user)
):
    # Only authenticated, active users can access
    return {"message": f"Hello {current_user.username}"}
```

#### 2. Resource Ownership Verification

```python
@router.get("/documents/{document_id}")
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Verify ownership
    if document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return document
```

#### 3. Self-Modification Only

```python
@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Users can only update their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own profile"
        )

    # Update logic...
```

### Security Best Practices

1. **Token Storage** (Client-side):
   - Store in memory for SPAs (most secure)
   - Use HttpOnly cookies for traditional apps
   - Avoid localStorage (vulnerable to XSS)

2. **Token Expiration**:
   - Short-lived access tokens (30 minutes)
   - Implement refresh tokens for long sessions
   - Clear tokens on logout

3. **HTTPS Only**:
   - Always use HTTPS in production
   - Prevents token interception

4. **CORS Configuration**:
   - Whitelist specific origins
   - Avoid `Access-Control-Allow-Origin: *`

5. **Rate Limiting**:
   - Implement on authentication endpoints
   - Prevents brute-force attacks

## Document Processing Pipeline

### Overview

The document processing pipeline transforms uploaded files into searchable vector embeddings for RAG-powered chat responses.

### Pipeline Stages

```
┌─────────────────┐
│  File Upload    │
│  (API Request)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  1. Validation  │
│  - File type    │
│  - File size    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  2. File Save   │
│  - UUID name    │
│  - Disk storage │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  3. DB Record   │
│  - Metadata     │
│  - processed=F  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  4. Background  │
│     Processing  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  5. Text        │
│     Extraction  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  6. Text        │
│     Chunking    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  7. Embedding   │
│     Generation  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  8. ChromaDB    │
│     Storage     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  9. Update DB   │
│  processed=True │
└─────────────────┘
```

### Stage Details

#### 1. File Upload & Validation

**Location**: `app/routers/documents.py:upload_document()`

```python
@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validation happens in document_processor.save_file()
    file_path, filename = await document_processor.save_file(file)
```

**Validation Rules**:
- **Allowed Types**: `.pdf`, `.docx`, `.txt`
- **Max Size**: 10MB (10,485,760 bytes)
- **Rejection**: HTTPException 400 if validation fails

#### 2. File Storage

**Location**: `app/services/document_processor.py:save_file()`

```python
async def save_file(self, file: UploadFile) -> tuple:
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(400, "File type not allowed")

    # Generate UUID filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Save file async
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()

        # Validate file size
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(400, "File too large")

        await f.write(content)

    return file_path, unique_filename
```

**Storage Location**: `uploads/` directory (configurable via `UPLOAD_DIR`)

**Filename Format**: `{UUID}.{original_extension}`
- Example: `a7f3e8b2-4c5d-6e7f-8a9b-0c1d2e3f4g5h.pdf`

#### 3. Database Record Creation

**Location**: `app/routers/documents.py:upload_document()`

```python
# Create document record
db_document = Document(
    filename=filename,
    original_filename=file.filename,
    file_path=file_path,
    file_size=os.path.getsize(file_path),
    content_type=file.content_type,
    owner_id=current_user.id,
    processed=False  # Will be updated after processing
)
db.add(db_document)
db.commit()
db.refresh(db_document)
```

#### 4. Background Processing

**Trigger**: FastAPI's `BackgroundTasks`

```python
# Queue processing task
background_tasks.add_task(
    process_document_task,
    file_path,
    db_document.id,
    db
)

# Return immediately
return db_document
```

**Why Background?**:
- Improves API response time
- Handles long-running operations
- User doesn't wait for processing to complete

#### 5. Text Extraction

**Location**: `app/services/document_processor.py:extract_text()`

**PDF Extraction**:
```python
import PyPDF2

def extract_text(self, file_path: str) -> str:
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
```

**DOCX Extraction**:
```python
from docx import Document

    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
```

**TXT Extraction**:
```python
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
```

**Error Handling**: HTTPException 500 on extraction failure

#### 6. Text Chunking

**Tool**: LangChain's `RecursiveCharacterTextSplitter`

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
```

**Parameters**:
- **chunk_size**: 1000 characters per chunk
- **chunk_overlap**: 200 characters overlap between chunks
- **separators**: Splits on paragraphs, then lines, then spaces

**Why Overlap?**:
- Preserves context across chunk boundaries
- Improves retrieval accuracy
- Prevents sentence fragmentation

**Example**:
```
Original text (2500 chars):
"Introduction to AI... [1000 chars] ...neural networks... [1000 chars] ...conclusion."

Chunks:
1. "Introduction to AI... [1000 chars] ...neural networks" (chars 0-1000)
2. "...previous 200 chars... neural networks... [800 chars]" (chars 800-1800)
3. "...previous 200 chars... [800 chars] ...conclusion." (chars 1600-2500)
```

#### 7. Embedding Generation

**Model**: `sentence-transformers/all-MiniLM-L6-v2`

**Initialization**:
```python
from langchain.embeddings import HuggingFaceEmbeddings

self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

**Model Characteristics**:
- **Dimensions**: 384
- **Max Tokens**: 256
- **Speed**: ~5ms per embedding on CPU
- **Quality**: Optimized for semantic search

**Process**:
```python
# For each chunk
for i, chunk in enumerate(chunks):
    embedding = self.embeddings.embed_query(chunk)
    # embedding is a list of 384 floats
```

#### 8. ChromaDB Storage

**Initialization**:
```python
import chromadb
from chromadb.config import Settings

self.chroma_client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

self.collection = self.chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)
```

**Storage Format**:
```python
self.collection.add(
    documents=chunks,  # List of text chunks
    embeddings=embeddings,  # List of 384-dim vectors
    metadatas=[
        {
            "document_id": document_id,
            "chunk_index": i,
            "file_path": file_path
        }
        for i in range(len(chunks))
    ],
    ids=[f"{document_id}_{i}" for i in range(len(chunks))]
)
```

**Persistence**: ChromaDB saves to disk at `CHROMA_DB_PATH` (default: `chroma_db/`)

#### 9. Status Update

**Location**: `app/services/document_processor.py:process_document()`

```python
def process_document(self, file_path: str, document_id: int) -> bool:
    try:
        # Extract, chunk, embed, store...

        # Update document status
        document = db.query(Document).filter(Document.id == document_id).first()
        document.processed = True
        db.commit()

        return True
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return False
```

### Performance Characteristics

**Processing Time** (approximate):
- 10-page PDF: ~5-10 seconds
- 50-page DOCX: ~15-30 seconds
- 100KB TXT: ~2-5 seconds

**Resource Usage**:
- CPU: High during embedding generation
- Memory: ~100MB per document during processing
- Disk: Original file + ~1KB per chunk in ChromaDB

### Error Handling

**Validation Errors** (immediate):
- 400: File type not allowed
- 400: File too large
- 422: No file provided

**Processing Errors** (background):
- Logged to console
- Document remains `processed=False`
- User can retry by reuploading

## Chat Service and RAG Integration

### Overview

The chat service orchestrates conversations by combining user messages, conversation history, and relevant document context through RAG (Retrieval-Augmented Generation).

### RAG Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Message                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ↓                     ↓
    ┌─────────────────────┐  ┌─────────────────────┐
    │  Conversation       │  │  Document Context   │
    │  History Retrieval  │  │  Retrieval (RAG)    │
    │  (Last 10 msgs)     │  │  (if use_documents) │
    └──────────┬──────────┘  └──────────┬──────────┘
               │                        │
               │   1. Query Embedding   │
               │   2. Vector Search     │
               │   3. Top 5 Chunks      │
               │                        │
               └────────┬───────────────┘
                        │
                        ↓
            ┌───────────────────────┐
            │  System Prompt        │
            │  Construction         │
            │  + Context            │
            │  + History            │
            └───────────┬───────────┘
                        │
                        ↓
            ┌───────────────────────┐
            │  OpenAI GPT-3.5       │
            │  API Call             │
            └───────────┬───────────┘
                        │
                        ↓
            ┌───────────────────────┐
            │  Save Response        │
            │  to Database          │
            └───────────┬───────────┘
                        │
                        ↓
            ┌───────────────────────┐
            │  Return ChatResponse  │
            │  + Sources            │
            └───────────────────────┘
```

### Key Components

#### 1. Message Processing

**Location**: `app/services/chat_service.py:generate_response()`

```python
async def generate_response(
    self,
    db: Session,
    request: ChatRequest,
    user: User
) -> ChatResponse:
    # Get or create session
    if request.session_id:
        session = self.get_session(db, request.session_id, user)
    else:
        session = self.create_session(db, user)

    # Save user message
    user_message = self.add_message(
        db,
        session.id,
        request.message,
        "user"
    )
```

#### 2. Document Context Retrieval (RAG)

**Conditional**: Only if `use_documents=true`

```python
    context = ""
    sources = []

    if request.use_documents:
        # Search for relevant document chunks
        relevant_docs = document_processor.search_documents(
            query=request.message,
            n_results=5
        )

        if relevant_docs:
            # Extract document IDs
            sources = list(set([
                doc["metadata"]["document_id"]
                for doc in relevant_docs
            ]))

            # Build context string
            context = "\n\n".join([
                f"Context from document {doc['metadata']['document_id']}:\n{doc['content']}"
                for doc in relevant_docs
            ])
```

**Vector Search**:
```python
# In document_processor.py
def search_documents(self, query: str, n_results: int = 5) -> List[dict]:
    # Generate query embedding
    query_embedding = self.embeddings.embed_query(query)

    # Search ChromaDB
    results = self.collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    # Format results
    return [
        {
            "content": doc,
            "metadata": meta,
            "distance": dist
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]
```

**Search Parameters**:
- **n_results**: Top 5 most similar chunks
- **Similarity Metric**: Cosine similarity
- **Distance**: Lower = more similar

#### 3. Conversation History

**Retrieval**: Last 10 messages for context

```python
    # Get conversation history
    conversation_history = self.get_session_messages(db, session.id)

    # Limit to last 10 messages
    conversation_history = conversation_history[-10:]

    # Format for OpenAI
    history_messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in conversation_history[:-1]  # Exclude current message
    ]
```

**Why Last 10?**:
- Balances context vs. token usage
- Prevents exceeding model's context window
- Maintains conversation coherence

#### 4. OpenAI API Integration

**System Prompt Construction**:
```python
async def _call_openai(
    self,
    user_message: str,
    context: str,
    conversation_history: List[dict]
) -> str:
    # Build system message with context
    system_message = {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }

    if context:
        system_message["content"] += (
            f"\n\nYou have access to the following information "
            f"from the user's documents:\n\n{context}\n\n"
            "Use this information to provide accurate and relevant responses."
        )

    # Construct messages array
    messages = [
        system_message,
        *conversation_history,
        {"role": "user", "content": user_message}
    ]
```

**API Call**:
```python
    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=self.model,  # gpt-3.5-turbo
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return self._fallback_response(user_message, context)
```

**API Parameters**:
- **model**: `gpt-3.5-turbo`
- **max_tokens**: 500 (limits response length)
- **temperature**: 0.7 (balanced creativity/determinism)

#### 5. Fallback Mechanism

**Triggered When**:
- OpenAI API key not configured
- API request fails (rate limit, network error, etc.)
- Authentication error

```python
def _fallback_response(self, user_message: str, context: str) -> str:
    """Return a fallback response when OpenAI is unavailable."""
    if context:
        return (
            f"I understand you're asking: '{user_message}'. "
            "I found some relevant information in your documents, "
            "but I cannot provide a detailed response at the moment. "
            "Please ensure the OpenAI API is configured correctly."
        )
    else:
        return (
            "I received your message but cannot generate a response "
            "at the moment. Please ensure the OpenAI API is configured correctly."
        )
```

**Benefits**:
- Graceful degradation
- User feedback on configuration issues
- Application remains functional

#### 6. Response Persistence

**Save to Database**:
```python
    # Save AI response
    assistant_message = self.add_message(
        db,
        session.id,
        ai_response,
        "assistant"
    )

    # Return response with metadata
    return ChatResponse(
        message=ai_response,
        session_id=session.id,
        sources=sources if request.use_documents else None
    )
```

### RAG vs. Non-RAG Comparison

#### Without Documents (`use_documents=false`)

```
User: "What is machine learning?"

System Prompt:
"You are a helpful AI assistant."

Response:
"Machine learning is a subset of artificial intelligence..."
(Generic response based on model's training)
```

#### With Documents (`use_documents=true`)

```
User: "What is machine learning?"

Retrieved Context:
"Context from document 1:
Machine learning in our organization focuses on supervised learning
for customer segmentation. We use gradient boosting algorithms...

Context from document 2:
Our ML pipeline includes data preprocessing, feature engineering..."

System Prompt:
"You are a helpful AI assistant.

You have access to the following information from the user's documents:
[Retrieved context above]

Use this information to provide accurate and relevant responses."

Response:
"Based on your documents, machine learning in your organization
primarily focuses on supervised learning for customer segmentation,
utilizing gradient boosting algorithms. Your ML pipeline emphasizes
data preprocessing and feature engineering..."
(Specific response grounded in user's documents)
```

### WebSocket Real-Time Chat

**Connection**: `ws://localhost:8000/api/chat/ws/{session_id}?token={jwt_token}`

**Server Handler**:
```python
@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    # Authenticate
    user = await authenticate_websocket(token, db)
    await websocket.accept()

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()

            # Process with RAG
            request = ChatRequest(
                message=data["message"],
                session_id=session_id,
                use_documents=data.get("use_documents", False)
            )

            response = await chat_service.generate_response(db, request, user)

            # Send response
            await websocket.send_json({
                "message": response.message,
                "session_id": response.session_id,
                "sources": response.sources
            })

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
```

### Performance Optimization

**Caching Strategies**:
- Cache conversation history in Redis
- Cache frequent document queries
- Reuse embedding model in memory

**Token Management**:
- Limit conversation history to 10 messages
- Set max_tokens=500 for responses
- Monitor total token usage per request

**Async Operations**:
- OpenAI API call is async
- Database queries use async session
- File I/O operations are async

## Error Handling

### HTTP Status Codes

The API uses standard HTTP status codes to indicate request outcomes:

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully (user registration) |
| 400 | Bad Request | Invalid input, file type not allowed, file too large |
| 401 | Unauthorized | Missing, invalid, or expired JWT token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Resource doesn't exist or user doesn't own it |
| 422 | Unprocessable Entity | Pydantic validation error, malformed JSON |
| 500 | Internal Server Error | Server-side error, database connection failure |

### Error Response Format

All errors return consistent JSON format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Example (401 Unauthorized)**:
```json
{
  "detail": "Could not validate credentials"
}
```

**Example (422 Validation Error)**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### Error Handling Patterns

#### 1. Authentication Errors

**Location**: `app/services/auth.py:get_current_user()`

```python
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
except JWTError:
    raise credentials_exception
```

**Triggers**:
- Missing Authorization header
- Malformed JWT token
- Expired token
- Invalid signature

#### 2. Authorization Errors

**Pattern**: Check ownership before allowing access

```python
@router.get("/documents/{document_id}")
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if document.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this document"
        )

    return document
```

#### 3. Validation Errors

**Automatic**: Pydantic validates all request bodies

```python
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
```

**Example Error**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ab", "email": "invalid", "password": "short"}'
```

**Response (422)**:
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "ensure this value has at least 3 characters",
      "type": "value_error.any_str.min_length"
    },
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    },
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

#### 4. File Upload Errors

**Location**: `app/services/document_processor.py:save_file()`

```python
# File type validation
file_ext = os.path.splitext(file.filename)[1].lower()
if file_ext not in settings.ALLOWED_FILE_TYPES:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"File type {file_ext} not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}"
    )

# File size validation
if len(content) > settings.MAX_FILE_SIZE:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
    )
```

#### 5. External API Errors

**Pattern**: Graceful fallback with user notification

```python
try:
    response = await openai.ChatCompletion.acreate(
        model=self.model,
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content

except openai.error.AuthenticationError:
    print("OpenAI API key invalid")
    return self._fallback_response(user_message, context)

except openai.error.RateLimitError:
    print("OpenAI rate limit exceeded")
    return "I'm experiencing high demand. Please try again in a moment."

except Exception as e:
    print(f"OpenAI API error: {str(e)}")
    return self._fallback_response(user_message, context)
```

#### 6. Database Errors

**Pattern**: Log and return generic error to user

```python
try:
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

except IntegrityError as e:
    db.rollback()
    print(f"Database integrity error: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Resource already exists or constraint violated"
    )

except Exception as e:
    db.rollback()
    print(f"Database error: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An error occurred while processing your request"
    )
```

### Global Exception Handler

**Location**: `app/main.py`

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )
```

### Logging Strategy

**Console Logging** (Development):
```python
print(f"Error processing document: {str(e)}")
print(f"OpenAI API error: {str(e)}")
print(f"User {user.username} uploaded document {document_id}")
```

**Production Logging** (Recommended):
```python
import logging

logger = logging.getLogger(__name__)

logger.error(f"Document processing failed: {str(e)}", exc_info=True)
logger.warning(f"OpenAI API rate limit reached")
logger.info(f"User {user.id} created session {session.id}")
```

## Testing

### Test Infrastructure

**Framework**: pytest with FastAPI TestClient

**Test Database**: SQLite in-memory (faster, isolated)

**Configuration**: `backend/tests/conftest.py`

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run specific test function
pytest tests/test_auth.py::test_register_user

# Run with coverage report
pytest --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Fixtures

**Location**: `backend/tests/conftest.py`

#### 1. `client` - Basic TestClient

```python
@pytest.fixture
def client():
    """Create a test client with test database."""
    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Yield test client
    with TestClient(app) as c:
        yield c

    # Cleanup
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
```

**Usage**:
```python
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
```

#### 2. `db` - Database Session

```python
@pytest.fixture
def db():
    """Create a fresh database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
```

**Usage**:
```python
def test_create_user(db):
    user = User(username="test", email="test@example.com")
    db.add(user)
    db.commit()
    assert user.id is not None
```

#### 3. `test_user_data` - Sample User

```python
@pytest.fixture
def test_user_data():
    """Standard test user data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
```

#### 4. `authenticated_client` - Client with JWT Token

```python
@pytest.fixture
def authenticated_client(client, test_user_data):
    """Test client with authentication token."""
    # Register user
    client.post("/api/auth/register", json=test_user_data)

    # Login
    login_response = client.post(
        "/api/auth/token",
        data={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]

    # Set authorization header
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
```

**Usage**:
```python
def test_get_current_user(authenticated_client):
    response = authenticated_client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

### Test Examples

#### Authentication Tests

**File**: `backend/tests/test_auth.py`

```python
def test_register_user(client, test_user_data):
    """Test user registration."""
    response = client.post("/api/auth/register", json=test_user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "hashed_password" not in data

def test_register_duplicate_user(client, test_user_data):
    """Test duplicate user registration fails."""
    # Register once
    client.post("/api/auth/register", json=test_user_data)

    # Try to register again
    response = client.post("/api/auth/register", json=test_user_data)

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

def test_login_user(client, test_user_data):
    """Test user login."""
    # Register
    client.post("/api/auth/register", json=test_user_data)

    # Login
    response = client.post(
        "/api/auth/token",
        data={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
```

#### Chat Tests

**File**: `backend/tests/test_chat.py`

```python
def test_create_chat_session(authenticated_client):
    """Test creating a new chat session."""
    response = authenticated_client.post("/api/chat/sessions?title=Test%20Chat")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Chat"
    assert "id" in data

def test_send_chat_message(authenticated_client):
    """Test sending a chat message."""
    response = authenticated_client.post(
        "/api/chat/",
        json={
            "message": "Hello, assistant!",
            "use_documents": False
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "session_id" in data
    assert isinstance(data["session_id"], int)

def test_get_session_messages(authenticated_client):
    """Test retrieving session messages."""
    # Send a message (creates session)
    send_response = authenticated_client.post(
        "/api/chat/",
        json={"message": "Test message"}
    )
    session_id = send_response.json()["session_id"]

    # Get messages
    response = authenticated_client.get(f"/api/chat/sessions/{session_id}/messages")

    assert response.status_code == 200
    messages = response.json()
    assert len(messages) >= 2  # User + assistant
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
```

### Testing Best Practices

#### 1. Test Isolation

```python
# Good: Each test is independent
def test_create_user(client):
    # Setup
    user_data = {"username": "unique_user", ...}

    # Test
    response = client.post("/api/auth/register", json=user_data)

    # Assert
    assert response.status_code == 201

# Bad: Tests depend on each other
def test_create_then_login():
    # Don't chain multiple operations in one test
    pass
```

#### 2. Use Fixtures

```python
# Good: Reuse common setup
def test_protected_endpoint(authenticated_client):
    response = authenticated_client.get("/api/auth/me")
    assert response.status_code == 200

# Bad: Repeat authentication in every test
def test_protected_endpoint(client):
    # Register
    client.post("/api/auth/register", ...)
    # Login
    login = client.post("/api/auth/token", ...)
    # Get token
    token = login.json()["access_token"]
    # Make request
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
```

#### 3. Test Edge Cases

```python
def test_login_invalid_credentials(client, test_user_data):
    """Test login with wrong password."""
    # Register
    client.post("/api/auth/register", json=test_user_data)

    # Try login with wrong password
    response = client.post(
        "/api/auth/token",
        data={
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

def test_upload_invalid_file_type(authenticated_client):
    """Test uploading disallowed file type."""
    files = {"file": ("malware.exe", b"fake content", "application/x-msdownload")}
    response = authenticated_client.post("/api/documents/upload", files=files)

    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()
```

#### 4. Mock External Services

```python
from unittest.mock import patch, MagicMock

def test_chat_with_openai_error(authenticated_client):
    """Test chat when OpenAI API fails."""
    with patch("openai.ChatCompletion.acreate") as mock_openai:
        mock_openai.side_effect = Exception("API Error")

        response = authenticated_client.post(
            "/api/chat/",
            json={"message": "Hello"}
        )

        assert response.status_code == 200
        # Should return fallback response
        assert "cannot generate a response" in response.json()["message"].lower()
```

### Coverage Goals

**Target**: > 80% code coverage

**Priority Areas**:
- Authentication: 100% (critical security component)
- API endpoints: 90%+ (user-facing functionality)
- Business logic: 85%+ (core features)
- Utilities: 70%+ (helper functions)

**Run Coverage Report**:
```bash
pytest --cov=app --cov-report=term-missing
```

## Code Structure

### Directory Organization

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   │
│   ├── routers/                   # API endpoints (HTTP layer)
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication routes
│   │   ├── users.py              # User management routes
│   │   ├── documents.py          # Document upload/management routes
│   │   └── chat.py               # Chat and messaging routes
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth.py               # Auth logic (hashing, tokens)
│   │   ├── database.py           # DB connection management
│   │   ├── chat_service.py       # Chat orchestration + RAG
│   │   └── document_processor.py # Document processing pipeline
│   │
│   ├── models/                    # Data layer
│   │   ├── __init__.py
│   │   ├── database.py           # SQLAlchemy ORM models
│   │   └── schemas.py            # Pydantic request/response schemas
│   │
│   └── utils/                     # Configuration & helpers
│       ├── __init__.py
│       └── config.py             # Settings management
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_auth.py              # Authentication tests
│   └── test_chat.py              # Chat functionality tests
│
├── uploads/                       # Uploaded files (runtime)
├── chroma_db/                     # Vector database (runtime)
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
├── .env.example                  # Example configuration
├── Dockerfile                     # Container definition
└── README.md                      # This file
```

### Layer Responsibilities

#### 1. Routers Layer (`app/routers/`)

**Purpose**: HTTP request handling and response serialization

**Responsibilities**:
- Define API endpoints
- Validate request data (Pydantic)
- Extract authentication tokens
- Call service layer functions
- Return HTTP responses

**Example**:
```python
@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate and save file
    file_path, filename = await document_processor.save_file(file)

    # Create database record
    db_document = Document(...)
    db.add(db_document)
    db.commit()

    # Queue background processing
    background_tasks.add_task(process_document_task, ...)

    return db_document
```

**Key Patterns**:
- Dependency injection for auth and database
- Async/await for I/O operations
- Background tasks for long-running operations

#### 2. Services Layer (`app/services/`)

**Purpose**: Business logic and orchestration

**Responsibilities**:
- Implement core business rules
- Orchestrate complex workflows
- Interact with external services (OpenAI, ChromaDB)
- Perform data transformations
- Handle errors gracefully

**Example**:
```python
class ChatService:
    async def generate_response(self, db, request, user):
        # Get/create session
        # Retrieve document context (RAG)
        # Get conversation history
        # Call OpenAI API
        # Save response
        # Return ChatResponse
```

**Benefits**:
- Testable (can mock dependencies)
- Reusable (called from multiple routers)
- Maintainable (logic isolated from HTTP layer)

#### 3. Models Layer (`app/models/`)

**Purpose**: Data definitions and validation

**Responsibilities**:
- Define database tables (SQLAlchemy ORM)
- Define request/response schemas (Pydantic)
- Specify validation rules
- Define relationships between entities

**database.py**:
```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    # ... other fields

    # Relationships
    documents = relationship("Document", back_populates="owner")
```

**schemas.py**:
```python
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
```

#### 4. Utils Layer (`app/utils/`)

**Purpose**: Configuration and shared utilities

**Responsibilities**:
- Load environment variables
- Provide application settings
- Define constants
- Shared helper functions

**config.py**:
```python
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
```

### Design Principles

#### 1. Separation of Concerns

Each layer has a single, well-defined purpose:
- Routers handle HTTP
- Services handle business logic
- Models handle data
- Utils handle configuration

#### 2. Dependency Injection

FastAPI's dependency system provides:
- Automatic injection of database sessions
- Authentication enforcement
- Testability (easy to override dependencies)

```python
# Router depends on get_current_user
async def get_documents(current_user: User = Depends(get_current_active_user)):
    # current_user is automatically injected
```

#### 3. Single Responsibility

Each module has one job:
- `auth.py` (routers): Only handles auth HTTP endpoints
- `auth.py` (services): Only handles auth logic
- `chat_service.py`: Only handles chat orchestration

#### 4. DRY (Don't Repeat Yourself)

Common logic is centralized:
- Authentication logic in `services/auth.py`
- Database session management in `services/database.py`
- Configuration in `utils/config.py`

## Dependencies

### Organized by Category

#### Web Framework

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.108.0 | Modern, high-performance web framework |
| uvicorn[standard] | 0.25.0 | ASGI server with WebSocket support |
| python-multipart | 0.0.6 | Multipart form data parsing (file uploads) |

#### Database & ORM

| Package | Version | Purpose |
|---------|---------|---------|
| sqlalchemy | 2.0.25 | SQL toolkit and ORM |
| psycopg2-binary | 2.9.9 | PostgreSQL adapter |
| alembic | 1.13.1 | Database migration tool |

#### Authentication & Security

| Package | Version | Purpose |
|---------|---------|---------|
| python-jose[cryptography] | 3.3.0 | JWT token generation and validation |
| passlib[bcrypt] | 1.7.4 | Password hashing with bcrypt |

#### Configuration Management

| Package | Version | Purpose |
|---------|---------|---------|
| python-dotenv | 1.0.0 | Load environment variables from .env |
| pydantic | 2.5.3 | Data validation and settings management |
| pydantic-settings | 2.1.0 | Settings management with Pydantic v2 |

#### AI & Machine Learning

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | 0.1.0 | LLM application framework |
| langchain-openai | 0.0.2 | OpenAI integration for LangChain |
| openai | (latest) | OpenAI API client (GPT-3.5-turbo) |
| sentence-transformers | 2.2.2 | Text embedding generation |

#### Vector Database

| Package | Version | Purpose |
|---------|---------|---------|
| chromadb | 0.4.22 | Vector database for embeddings |

#### Document Processing

| Package | Version | Purpose |
|---------|---------|---------|
| pypdf2 | 3.0.1 | PDF text extraction |
| python-docx | 1.1.0 | DOCX text extraction |

#### Async & I/O

| Package | Version | Purpose |
|---------|---------|---------|
| aiofiles | 23.2.0 | Async file operations |
| httpx | 0.26.0 | Async HTTP client |
| websockets | (latest) | WebSocket protocol implementation |

#### Caching

| Package | Version | Purpose |
|---------|---------|---------|
| redis | 5.0.1 | Redis client for caching |

#### Testing

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | (dev) | Testing framework |
| pytest-cov | (dev) | Coverage reporting |

### Installation

**Install all dependencies**:
```bash
pip install -r requirements.txt
```

**Install with development dependencies**:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio
```

**Install in virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Dependency Updates

**Check for outdated packages**:
```bash
pip list --outdated
```

**Update specific package**:
```bash
pip install --upgrade fastapi
```

**Regenerate requirements.txt**:
```bash
pip freeze > requirements.txt
```

## Development Workflow

### Local Development

#### 1. Start Development Server

```bash
# With hot-reload (auto-restarts on code changes)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# With custom port
uvicorn app.main:app --reload --port 8001

# With log level
uvicorn app.main:app --reload --log-level debug
```

#### 2. Access Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### 3. Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_auth.py -v

# Watch mode (rerun on file changes)
ptw -- tests/
```

#### 4. Code Quality

**Linting**:
```bash
# Install flake8
pip install flake8

# Run linter
flake8 app tests

# With specific config
flake8 app --max-line-length=120 --exclude=venv
```

**Formatting**:
```bash
# Install black
pip install black

# Format code
black app tests

# Check formatting (no changes)
black --check app tests
```

**Type Checking**:
```bash
# Install mypy
pip install mypy

# Run type checker
mypy app
```

### Docker Development

#### 1. Build and Run

```bash
# Development with hot-reload
docker-compose -f docker-compose.dev.yml up --build

# Production build
docker-compose up --build

# Detached mode (background)
docker-compose up -d

# Rebuild specific service
docker-compose up --build backend
```

#### 2. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

#### 3. Execute Commands in Container

```bash
# Open shell in running container
docker-compose exec backend bash

# Run tests in container
docker-compose exec backend pytest

# Run database migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "Add new field"
```

#### 4. Database Operations

```bash
# Access PostgreSQL shell
docker-compose exec postgres psql -U chatbot -d chatbot_db

# Backup database
docker-compose exec postgres pg_dump -U chatbot chatbot_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U chatbot chatbot_db < backup.sql
```

#### 5. Cleanup

```bash
# Stop containers
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v

# Remove all containers, networks, and images
docker-compose down --rmi all -v
```

### Common Development Commands

#### Database Management

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

#### Dependency Management

```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt

# Uninstall package
pip uninstall package-name
```

#### Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit environment file
nano .env  # or vim .env, code .env, etc.

# Load environment variables (in shell)
export $(cat .env | xargs)
```

### Debugging

#### 1. Python Debugger (pdb)

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint() (Python 3.7+)
breakpoint()
```

#### 2. Print Debugging

```python
# Log to console
print(f"User ID: {user.id}")
print(f"Request data: {request.json()}")

# Pretty print JSON
import json
print(json.dumps(data, indent=2))
```

#### 3. FastAPI Debug Mode

```python
# In app/main.py
app = FastAPI(debug=True)  # Enables detailed error pages
```

#### 4. Database Query Debugging

```python
# Enable SQL logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Performance Profiling

```bash
# Install profiling tools
pip install py-spy

# Profile running application
py-spy top --pid <process_id>

# Generate flame graph
py-spy record -o profile.svg -- python -m uvicorn app.main:app
```

## Contributing

### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/AI-Chatbot.git
   cd AI-Chatbot/backend
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up development environment** (see Setup and Installation)

### Coding Standards

#### Python Style Guide

- **PEP 8**: Follow Python's official style guide
- **Line Length**: Maximum 120 characters
- **Imports**: Group and order imports
  ```python
  # Standard library
  import os
  import sys

  # Third-party
  from fastapi import FastAPI
  from sqlalchemy import Column

  # Local
  from app.models import User
  from app.utils.config import settings
  ```
- **Naming Conventions**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

#### Code Quality

**Required**:
- All new code must have tests
- Tests must pass: `pytest`
- Code must be formatted: `black app tests`
- No linting errors: `flake8 app tests`

**Recommended**:
- Type hints for function signatures
- Docstrings for public functions/classes
- Comments for complex logic

#### Example Function

```python
from typing import Optional
from sqlalchemy.orm import Session
from app.models.database import User

def get_user_by_username(
    db: Session,
    username: str
) -> Optional[User]:
    """
    Retrieve a user by username.

    Args:
        db: Database session
        username: Username to search for

    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()
```

### Pull Request Process

#### 1. Before Submitting

- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `black app tests`
- [ ] No linting errors: `flake8 app tests`
- [ ] New features have tests
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages are clear and descriptive

#### 2. Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting (no code changes)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat: Add document search filtering by date

- Added created_at parameter to search endpoint
- Updated tests to cover new functionality
- Added documentation for new query parameter

Closes #123
```

#### 3. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

#### 4. Review Process

1. Submit PR with clear description
2. Automated checks run (tests, linting)
3. Code review by maintainers
4. Address feedback
5. Approval and merge

### Development Best Practices

#### 1. Small, Focused Changes

- One feature/fix per PR
- Keep PRs under 400 lines when possible
- Break large features into smaller PRs

#### 2. Write Tests First (TDD)

```python
# 1. Write failing test
def test_new_feature(client):
    response = client.get("/new-endpoint")
    assert response.status_code == 200

# 2. Implement feature
@router.get("/new-endpoint")
def new_endpoint():
    return {"message": "success"}

# 3. Test passes
```

#### 3. Documentation

- Update README.md for new features
- Add docstrings to new functions
- Update API documentation
- Add code comments for complex logic

#### 4. Security

- Never commit secrets (.env files, API keys)
- Use environment variables for sensitive data
- Validate all user input
- Use parameterized queries (SQLAlchemy handles this)
- Keep dependencies updated

### Questions or Issues?

- **Bug Reports**: Open an issue with reproduction steps
- **Feature Requests**: Open an issue with use case description
- **Questions**: Use GitHub Discussions or contact maintainers

---

## License

[Specify your license here]

## Support

For questions or support, please open an issue on GitHub.

---

**Generated**: 2025-11-10
**Version**: 1.0.0
