"""
Seed script for blog system data.

This script populates the database with sample authors and blog posts.
Run this after applying migrations to have demo data for the blog system.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.models.database import Author, Post, Base
from app.services.database import engine, SessionLocal


def seed_authors(db: Session) -> dict[str, Author]:
    """
    Create sample authors if they don't already exist.

    Args:
        db: Database session

    Returns:
        Dictionary mapping author names to Author objects
    """
    authors_data = [
        {
            "name": "Sarah Chen",
            "email": "sarah.chen@example.com",
            "bio": "Full-stack developer with 8+ years of experience in Python and React. Passionate about building scalable web applications and sharing knowledge through technical writing.",
            "profile_picture_url": "https://i.pravatar.cc/150?img=1"
        },
        {
            "name": "Marcus Rodriguez",
            "email": "marcus.rodriguez@example.com",
            "bio": "AI/ML engineer focused on natural language processing and chatbot development. Advocate for open-source software and ethical AI practices.",
            "profile_picture_url": "https://i.pravatar.cc/150?img=12"
        },
        {
            "name": "Aisha Patel",
            "email": "aisha.patel@example.com",
            "bio": "DevOps specialist and cloud architecture expert. Helps teams implement CI/CD pipelines and containerized deployments. Speaker at tech conferences.",
            "profile_picture_url": "https://i.pravatar.cc/150?img=5"
        },
        {
            "name": "James O'Connor",
            "email": "james.oconnor@example.com",
            "bio": "Database architect with expertise in PostgreSQL and vector databases. Specializes in optimizing queries and designing efficient data models.",
            "profile_picture_url": "https://i.pravatar.cc/150?img=8"
        },
        {
            "name": "Luna Kim",
            "email": "luna.kim@example.com",
            "bio": "UX engineer bridging design and development. Creates accessible, user-friendly interfaces with modern frameworks like React and TypeScript.",
            "profile_picture_url": "https://i.pravatar.cc/150?img=9"
        }
    ]

    authors = {}

    for author_data in authors_data:
        # Check if author already exists
        existing_author = db.query(Author).filter(
            Author.email == author_data["email"]
        ).first()

        if existing_author:
            print(f"Author {author_data['name']} already exists, skipping...")
            authors[author_data["name"]] = existing_author
        else:
            author = Author(**author_data)
            db.add(author)
            authors[author_data["name"]] = author
            print(f"Created author: {author_data['name']}")

    db.commit()

    # Refresh to get IDs
    for author in authors.values():
        db.refresh(author)

    return authors


def seed_posts(db: Session, authors: dict[str, Author]) -> None:
    """
    Create sample blog posts if they don't already exist.

    Args:
        db: Database session
        authors: Dictionary mapping author names to Author objects
    """
    posts_data = [
        {
            "title": "Building a Full-Stack AI Chatbot with FastAPI and React",
            "content": """In this comprehensive guide, we'll walk through building a production-ready AI chatbot application using modern web technologies.

## Architecture Overview

Our chatbot uses FastAPI for the backend, providing high-performance async endpoints for real-time chat interactions. The frontend is built with React and TypeScript for type safety and excellent developer experience.

## Key Features

- **Document Upload**: Users can upload PDFs, DOCX, and text files
- **RAG (Retrieval-Augmented Generation)**: Context from uploaded documents enhances AI responses
- **Vector Storage**: ChromaDB stores embeddings for semantic search
- **Authentication**: JWT-based auth with password hashing

## Tech Stack

- Backend: FastAPI, SQLAlchemy, ChromaDB
- Frontend: React, TypeScript, Tailwind CSS
- AI: OpenAI GPT models with LangChain
- Database: PostgreSQL

Stay tuned for the next post where we'll dive into implementing the RAG pipeline!""",
            "author": "Sarah Chen",
            "status": "published",
            "published_at": datetime.now() - timedelta(days=7),
            "tags": "python,fastapi,react,ai,chatbot",
            "category": "Tutorials"
        },
        {
            "title": "Understanding Retrieval-Augmented Generation (RAG)",
            "content": """RAG is revolutionizing how we build AI applications by combining the power of large language models with external knowledge sources.

## What is RAG?

Retrieval-Augmented Generation allows LLMs to access specific information beyond their training data. Instead of relying solely on the model's parametric knowledge, RAG retrieves relevant documents and injects them as context.

## How It Works

1. **Document Processing**: Text is split into chunks
2. **Embedding**: Each chunk is converted to a vector
3. **Storage**: Vectors are stored in a vector database
4. **Query**: User questions are embedded using the same model
5. **Retrieval**: Similar chunks are found using cosine similarity
6. **Generation**: Retrieved context is added to the LLM prompt

## Benefits

- Up-to-date information without retraining
- Source attribution and transparency
- Domain-specific knowledge integration
- Reduced hallucinations

In our chatbot, we use ChromaDB for vector storage and sentence-transformers for embeddings.""",
            "author": "Marcus Rodriguez",
            "status": "published",
            "published_at": datetime.now() - timedelta(days=5),
            "tags": "ai,rag,nlp,machine-learning",
            "category": "AI/ML"
        },
        {
            "title": "Containerizing Your FastAPI Application with Docker",
            "content": """Learn how to containerize your FastAPI application for consistent deployments across environments.

## Why Docker?

Docker ensures your application runs the same way everywhere - from your laptop to production servers. It packages your code, dependencies, and runtime into a single container image.

## Multi-Stage Builds

Use multi-stage builds to keep your production images lean:

```dockerfile
# Build stage
FROM python:3.11 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

## Docker Compose for Development

Use docker-compose.yml to orchestrate multiple services:
- FastAPI backend
- PostgreSQL database
- Redis for caching
- ChromaDB for vector storage

This setup ensures all developers have identical environments.""",
            "author": "Aisha Patel",
            "status": "published",
            "published_at": datetime.now() - timedelta(days=3),
            "tags": "docker,devops,deployment,containers",
            "category": "DevOps"
        },
        {
            "title": "Database Design for Chat Applications",
            "content": """Designing an efficient database schema for chat applications requires careful consideration of relationships, indexes, and query patterns.

## Core Models

Our chat system uses four main tables:

- **Users**: Authentication and profile data
- **ChatSessions**: Conversation containers
- **ChatMessages**: Individual messages with role and content
- **Documents**: Uploaded files with processing status

## Key Design Decisions

### Indexes
We index foreign keys and frequently queried fields like timestamps and status columns.

### Relationships
SQLAlchemy's `relationship()` provides convenient navigation:
- User.chat_sessions to get all sessions for a user
- ChatSession.messages to get messages in a session

### Timestamps
Using `server_default=func.now()` ensures consistent timestamps from the database.

## Performance Considerations

- Limit message queries to prevent loading entire chat history
- Use pagination for long conversations
- Consider archiving old messages to a separate table

Next post: Implementing real-time chat with WebSockets!""",
            "author": "James O'Connor",
            "status": "published",
            "published_at": datetime.now() - timedelta(days=2),
            "tags": "database,postgresql,sqlalchemy,design",
            "category": "Database"
        },
        {
            "title": "Best Practices for JWT Authentication in FastAPI",
            "content": """Implementing secure authentication is critical for any web application. Let's explore JWT authentication in FastAPI.

## Why JWT?

JSON Web Tokens (JWT) are stateless, scalable, and work great with modern SPAs and mobile apps.

## Implementation

1. **Password Hashing**: Use bcrypt or passlib
2. **Token Generation**: Create JWT with user claims and expiration
3. **Token Validation**: Verify signature and check expiration
4. **Dependency Injection**: Use FastAPI dependencies for protected routes

## Security Tips

- Use strong secrets (256-bit minimum)
- Set reasonable expiration times (15-60 minutes)
- Consider refresh tokens for longer sessions
- Never store sensitive data in JWT payload
- Use HTTPS in production

## Code Example

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate token and return user
    pass
```

Stay secure!""",
            "author": "Sarah Chen",
            "status": "published",
            "published_at": datetime.now() - timedelta(days=1),
            "tags": "security,authentication,jwt,fastapi",
            "category": "Security"
        },
        {
            "title": "Creating Accessible React Components",
            "content": """Accessibility should be a first-class concern when building React applications. Here's how to make your components usable for everyone.

## ARIA Attributes

Use appropriate ARIA roles and labels:

```jsx
<button
  aria-label="Close dialog"
  aria-pressed={isPressed}
  onClick={handleClick}
>
  <Icon name="close" aria-hidden="true" />
</button>
```

## Keyboard Navigation

Ensure all interactive elements are keyboard accessible:
- Use semantic HTML (`<button>` not `<div onClick>`)
- Implement focus management for modals and dropdowns
- Provide skip links for navigation

## Color and Contrast

- Maintain WCAG AA contrast ratios (4.5:1 for text)
- Don't rely solely on color to convey information
- Test with colorblindness simulators

## Screen Reader Testing

Test with actual screen readers:
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (macOS/iOS)

Making your app accessible makes it better for everyone!""",
            "author": "Luna Kim",
            "status": "published",
            "published_at": datetime.now() - timedelta(hours=12),
            "tags": "react,accessibility,a11y,frontend",
            "category": "Frontend"
        },
        {
            "title": "Optimizing Vector Search with ChromaDB",
            "content": """Vector databases are essential for modern AI applications. Let's explore how to optimize ChromaDB for production use.

## What is ChromaDB?

ChromaDB is an open-source embedding database designed for AI applications. It stores vector embeddings and provides fast similarity search.

## Configuration

### Persistence
Use persistent storage instead of in-memory:

```python
client = chromadb.PersistentClient(path="./chroma_db")
```

### Collections
Create collections with appropriate distance metrics:
- Cosine similarity for normalized embeddings
- L2 distance for absolute distances
- Inner product for similarity scoring

## Performance Tips

1. **Batch Operations**: Add documents in batches of 100-1000
2. **Indexing**: ChromaDB automatically indexes, but larger datasets benefit from HNSW
3. **Filtering**: Use metadata filters before similarity search
4. **Caching**: Cache frequent queries at the application level

## Monitoring

Track these metrics:
- Query latency
- Collection size
- Disk usage

Stay tuned for advanced RAG patterns!""",
            "author": "Marcus Rodriguez",
            "status": "draft",
            "published_at": None,
            "tags": "chromadb,vector-database,ai,performance",
            "category": "AI/ML"
        },
        {
            "title": "Database Migrations with Alembic",
            "content": """Database migrations are crucial for maintaining schema consistency across environments. Alembic is the go-to tool for SQLAlchemy projects.

## Why Migrations?

Migrations allow you to:
- Version control your database schema
- Apply changes consistently across environments
- Rollback changes if needed
- Track schema evolution over time

## Getting Started

Initialize Alembic:
```bash
alembic init alembic
```

Configure `alembic.ini` and `env.py` to connect to your database and import models.

## Common Operations

### Creating Migrations
```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "Add user preferences"

# Create empty migration
alembic revision -m "Add custom indexes"
```

### Applying Migrations
```bash
# Upgrade to latest
alembic upgrade head

# Rollback one version
alembic downgrade -1
```

## Best Practices

- Always review auto-generated migrations
- Test rollbacks before deploying
- Use descriptive migration messages
- Keep migrations focused and atomic

I'll be publishing more about data migrations and handling production deployments next!""",
            "author": "James O'Connor",
            "status": "draft",
            "published_at": None,
            "tags": "database,migrations,alembic,sqlalchemy",
            "category": "Database"
        },
        {
            "title": "CI/CD Pipelines for Python Applications",
            "content": """Setting up automated testing and deployment pipelines ensures code quality and streamlines releases.

## GitHub Actions Workflow

Here's a basic CI pipeline:

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app tests/
```

## Testing Strategy

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test API endpoints
- **E2E Tests**: Test full user workflows

## Deployment

### Docker Registry
Build and push images on main branch:
```yaml
- run: docker build -t myapp:latest .
- run: docker push myapp:latest
```

### Deployment Targets
- Heroku
- AWS ECS
- Google Cloud Run
- DigitalOcean App Platform

## Monitoring

Set up alerts for:
- Failed builds
- Test failures
- Deployment errors

Automate everything!""",
            "author": "Aisha Patel",
            "status": "draft",
            "published_at": None,
            "tags": "cicd,github-actions,testing,automation",
            "category": "DevOps"
        },
        {
            "title": "TypeScript Best Practices for React Projects",
            "content": """TypeScript adds type safety to JavaScript, catching errors at compile time and improving developer experience.

## Type Definitions

Define clear interfaces for your data:

```typescript
interface ChatMessage {
  id: number;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}
```

## Props Typing

Use proper prop types:

```typescript
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

const Button: React.FC<ButtonProps> = ({
  onClick,
  children,
  variant = 'primary'
}) => {
  return <button onClick={onClick}>{children}</button>;
};
```

## Hooks Typing

Type your hooks correctly:

```typescript
const [messages, setMessages] = useState<ChatMessage[]>([]);
const [loading, setLoading] = useState<boolean>(false);
```

## API Responses

Define response types for API calls:

```typescript
interface ApiResponse<T> {
  data: T;
  error?: string;
}
```

Type safety prevents bugs and makes refactoring safer!""",
            "author": "Luna Kim",
            "status": "published",
            "published_at": datetime.now() - timedelta(hours=6),
            "tags": "typescript,react,frontend,types",
            "category": "Frontend"
        }
    ]

    for post_data in posts_data:
        author_name = post_data.pop("author")
        author = authors[author_name]

        # Check if post already exists (check by title and author)
        existing_post = db.query(Post).filter(
            Post.title == post_data["title"],
            Post.author_id == author.id
        ).first()

        if existing_post:
            print(f"Post '{post_data['title'][:50]}...' already exists, skipping...")
            continue

        post = Post(**post_data, author_id=author.id)
        db.add(post)
        print(f"Created post: {post_data['title']}")

    db.commit()


def check_existing_data(db: Session) -> tuple[int, int]:
    """
    Check if seed data already exists.

    Args:
        db: Database session

    Returns:
        Tuple of (author_count, post_count)
    """
    author_count = db.query(Author).count()
    post_count = db.query(Post).count()
    return author_count, post_count


def seed_database() -> None:
    """
    Main function to seed the database with blog data.

    Creates sample authors and posts if they don't already exist.
    Safe to run multiple times - checks for existing data.
    """
    # Create database session
    db = SessionLocal()

    try:
        print("=" * 60)
        print("Blog System Seed Data Script")
        print("=" * 60)
        print()

        # Check existing data
        author_count, post_count = check_existing_data(db)
        print(f"Current database state:")
        print(f"  - Authors: {author_count}")
        print(f"  - Posts: {post_count}")
        print()

        # Seed authors
        print("Seeding authors...")
        print("-" * 60)
        authors = seed_authors(db)
        print()

        # Seed posts
        print("Seeding posts...")
        print("-" * 60)
        seed_posts(db, authors)
        print()

        # Show final counts
        author_count, post_count = check_existing_data(db)
        print("=" * 60)
        print(f"Seeding completed!")
        print(f"Final database state:")
        print(f"  - Authors: {author_count}")
        print(f"  - Posts: {post_count}")
        print("=" * 60)

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
