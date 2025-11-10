"""
Database seed script for blog posts and authors.

Run this script to populate the database with sample blog posts and authors for testing.
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, Author, BlogPost
from app.utils.config import settings


def seed_data():
    """Seed the database with sample blog posts and authors."""
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create session
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_authors = db.query(Author).count()
        if existing_authors > 0:
            print(f"Database already has {existing_authors} authors. Skipping seed.")
            return

        print("Seeding database with sample blog data...")

        # Create sample authors
        authors_data = [
            {
                "name": "Jane Smith",
                "bio": "Jane is a senior software engineer with over 10 years of experience in full-stack development. She specializes in Python, React, and cloud architecture.",
                "profile_picture_url": "https://i.pravatar.cc/150?img=1"
            },
            {
                "name": "John Doe",
                "bio": "John is a machine learning engineer passionate about AI and natural language processing. He loves sharing his knowledge through technical writing.",
                "profile_picture_url": "https://i.pravatar.cc/150?img=2"
            },
            {
                "name": "Sarah Johnson",
                "bio": "Sarah is a DevOps specialist and cloud architect. She enjoys writing about infrastructure as code, CI/CD pipelines, and best practices in software deployment.",
                "profile_picture_url": "https://i.pravatar.cc/150?img=3"
            }
        ]

        authors = []
        for author_data in authors_data:
            author = Author(**author_data)
            db.add(author)
            authors.append(author)

        db.commit()
        print(f"Created {len(authors)} authors")

        # Create sample blog posts
        posts_data = [
            {
                "title": "Getting Started with FastAPI and React",
                "excerpt": "Learn how to build a modern full-stack application using FastAPI for the backend and React for the frontend.",
                "content": """# Getting Started with FastAPI and React

In this tutorial, we'll explore how to build a modern full-stack application using FastAPI for the backend and React for the frontend. This combination provides a powerful and efficient way to create web applications.

## Why FastAPI?

FastAPI is a modern, fast web framework for building APIs with Python 3.7+. It's built on top of Starlette and Pydantic, offering:

- **High performance**: Comparable to NodeJS and Go
- **Easy to use**: Intuitive and easy to learn
- **Automatic API documentation**: Built-in Swagger UI and ReDoc
- **Type safety**: Leverages Python type hints for validation

## Why React?

React is a popular JavaScript library for building user interfaces:

- **Component-based architecture**: Build encapsulated components
- **Virtual DOM**: Efficient updates and rendering
- **Rich ecosystem**: Vast collection of libraries and tools
- **Strong community support**: Extensive resources and packages

## Setting Up Your Project

First, let's set up our backend with FastAPI:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install FastAPI and Uvicorn
pip install fastapi uvicorn sqlalchemy
```

Next, set up your React frontend:

```bash
# Create React app
npx create-react-app frontend
cd frontend
npm install axios
```

## Building Your First Endpoint

Here's a simple FastAPI endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}
```

## Connecting React to FastAPI

In your React component, use axios to fetch data:

```javascript
import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/api/hello')
      .then(response => setMessage(response.data.message));
  }, []);

  return <div>{message}</div>;
}
```

## Conclusion

FastAPI and React make a powerful combination for building modern web applications. FastAPI provides a fast, type-safe backend, while React offers a flexible, component-based frontend. Together, they enable you to build scalable, maintainable applications efficiently.

Stay tuned for more advanced topics like authentication, database integration, and deployment!""",
                "author_id": 1,
                "publication_date": datetime.now() - timedelta(days=2)
            },
            {
                "title": "Understanding RAG: Retrieval-Augmented Generation",
                "excerpt": "Explore how RAG combines retrieval systems with large language models to provide more accurate and contextual responses.",
                "content": """# Understanding RAG: Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) is a powerful technique that enhances large language models by combining them with external knowledge retrieval systems.

## What is RAG?

RAG is an AI framework that improves the accuracy and relevance of responses by:

1. **Retrieving** relevant information from a knowledge base
2. **Augmenting** the prompt with this retrieved context
3. **Generating** a response using the enhanced prompt

## Why Use RAG?

Traditional language models have several limitations:

- **Static knowledge**: Training data has a cutoff date
- **Hallucinations**: May generate plausible but incorrect information
- **No source attribution**: Can't cite where information comes from

RAG addresses these issues by grounding responses in actual documents.

## How RAG Works

### 1. Document Ingestion

First, documents are processed and stored:

```python
# Extract text from documents
text = extract_text(document)

# Split into chunks
chunks = text_splitter.split_text(text)

# Generate embeddings
embeddings = embedding_model.encode(chunks)

# Store in vector database
vector_db.add(chunks, embeddings)
```

### 2. Query Processing

When a user asks a question:

```python
# Generate query embedding
query_embedding = embedding_model.encode(query)

# Search for similar chunks
relevant_chunks = vector_db.search(query_embedding, top_k=5)

# Combine context with query
enhanced_prompt = f"""
Context: {relevant_chunks}
Question: {query}
"""
```

### 3. Response Generation

The LLM generates a response using the enhanced prompt:

```python
response = llm.generate(enhanced_prompt)
```

## Key Components

### Vector Databases

Popular options include:

- **ChromaDB**: Lightweight, embedded database
- **Pinecone**: Managed vector database service
- **Weaviate**: Open-source vector search engine
- **FAISS**: Facebook's similarity search library

### Embedding Models

Common choices:

- **Sentence Transformers**: Versatile and efficient
- **OpenAI Embeddings**: High-quality, API-based
- **Cohere Embeddings**: Multilingual support

## Best Practices

1. **Chunk size matters**: Balance between context and precision (typically 500-1000 chars)
2. **Overlap chunks**: Prevent information loss at boundaries
3. **Metadata filtering**: Add filters for better retrieval
4. **Hybrid search**: Combine semantic and keyword search
5. **Reranking**: Use a reranker model to improve results

## Conclusion

RAG is a game-changer for building AI applications that need accurate, up-to-date information. By combining retrieval with generation, you can create chatbots, question-answering systems, and knowledge assistants that are both powerful and reliable.

In future posts, we'll dive deeper into implementing RAG systems with practical examples!""",
                "author_id": 2,
                "publication_date": datetime.now() - timedelta(days=5)
            },
            {
                "title": "Docker Best Practices for Development",
                "excerpt": "Essential Docker practices to improve your development workflow and container management.",
                "content": """# Docker Best Practices for Development

Docker has revolutionized how we develop and deploy applications. Here are essential best practices to make your Docker workflow more efficient and secure.

## 1. Use Multi-Stage Builds

Multi-stage builds reduce image size and improve security:

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

## 2. Optimize Layer Caching

Order Dockerfile instructions from least to most frequently changing:

```dockerfile
# Good: Dependencies change less frequently than source code
COPY package*.json ./
RUN npm install
COPY . .

# Bad: Source changes invalidate dependency cache
COPY . .
RUN npm install
```

## 3. Use .dockerignore

Exclude unnecessary files from your build context:

```
node_modules
npm-debug.log
.git
.env
*.md
```

## 4. Don't Run as Root

Create a non-root user:

```dockerfile
FROM node:18-alpine

# Create app user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Set working directory and ownership
WORKDIR /app
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

CMD ["node", "index.js"]
```

## 5. Use Specific Base Images

Avoid the `latest` tag:

```dockerfile
# Good
FROM python:3.11-slim

# Bad
FROM python:latest
```

## 6. Health Checks

Add health checks to your containers:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

## 7. Environment Variables

Use environment variables for configuration:

```dockerfile
ENV NODE_ENV=production
ENV PORT=3000

# Or use docker-compose.yml
services:
  app:
    environment:
      - NODE_ENV=production
      - PORT=3000
```

## 8. Volume Management

Use named volumes for persistent data:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 9. Networking Best Practices

Use custom networks to isolate services:

```yaml
services:
  frontend:
    networks:
      - public

  backend:
    networks:
      - public
      - private

  database:
    networks:
      - private

networks:
  public:
  private:
```

## 10. Resource Limits

Set memory and CPU limits:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M
```

## Development vs Production

Use different Dockerfiles or docker-compose files:

```bash
# Development
docker-compose -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.prod.yml up
```

## Security Scanning

Regularly scan your images:

```bash
# Using Docker Scout
docker scout quickview myimage:latest

# Using Trivy
trivy image myimage:latest
```

## Conclusion

Following these Docker best practices will help you create more efficient, secure, and maintainable containerized applications. Remember to continuously learn and adapt as Docker evolves!

Happy containerizing!""",
                "author_id": 3,
                "publication_date": datetime.now() - timedelta(days=7)
            },
            {
                "title": "Python Asyncio: A Deep Dive",
                "excerpt": "Master asynchronous programming in Python with asyncio for building high-performance applications.",
                "content": """# Python Asyncio: A Deep Dive

Asynchronous programming in Python can dramatically improve the performance of I/O-bound applications. Let's explore asyncio and how to use it effectively.

## What is Asyncio?

Asyncio is Python's built-in library for writing concurrent code using the async/await syntax. It's particularly useful for:

- Web servers and clients
- Database operations
- File I/O
- Network operations

## Basic Concepts

### Coroutines

A coroutine is a function defined with `async def`:

```python
async def fetch_data():
    await asyncio.sleep(1)
    return "Data fetched"
```

### The Event Loop

The event loop runs asynchronous tasks:

```python
import asyncio

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

## Concurrent Execution

Run multiple coroutines concurrently:

```python
async def fetch_user(user_id):
    await asyncio.sleep(1)
    return f"User {user_id}"

async def main():
    # Run concurrently
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )
    print(users)
```

## Working with HTTP Requests

Use aiohttp for async HTTP:

```python
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, 'https://example.com')
        print(html)
```

## Database Operations

Use async database drivers:

```python
import asyncpg

async def get_users():
    conn = await asyncpg.connect(database='mydb')
    try:
        users = await conn.fetch('SELECT * FROM users')
        return users
    finally:
        await conn.close()
```

## Error Handling

Handle exceptions in async code:

```python
async def risky_operation():
    try:
        await some_async_function()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await cleanup()
```

## Tasks and Scheduling

Create and manage tasks:

```python
async def background_task():
    while True:
        await asyncio.sleep(60)
        print("Running background task")

async def main():
    # Create task
    task = asyncio.create_task(background_task())

    # Do other work
    await asyncio.sleep(180)

    # Cancel task
    task.cancel()
```

## Performance Considerations

### When to Use Asyncio

Good for:
- I/O-bound operations
- Network requests
- Database queries
- File operations

Not ideal for:
- CPU-bound operations (use multiprocessing instead)
- Simple scripts
- Synchronous libraries

## Common Patterns

### Timeout

```python
async def fetch_with_timeout():
    try:
        return await asyncio.wait_for(fetch_data(), timeout=5.0)
    except asyncio.TimeoutError:
        print("Operation timed out")
```

### Semaphore

Limit concurrent operations:

```python
sem = asyncio.Semaphore(10)

async def limited_fetch(url):
    async with sem:
        return await fetch_url(url)
```

## FastAPI Integration

FastAPI makes async easy:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await fetch_user_from_db(user_id)
    return user
```

## Conclusion

Asyncio is a powerful tool for building high-performance Python applications. By understanding coroutines, the event loop, and concurrent execution patterns, you can write efficient asynchronous code that handles I/O operations gracefully.

Start small, test thoroughly, and gradually introduce async patterns into your applications!""",
                "author_id": 1,
                "publication_date": datetime.now() - timedelta(days=10)
            },
            {
                "title": "Building Scalable Microservices",
                "excerpt": "Learn the principles and patterns for designing and implementing scalable microservices architectures.",
                "content": """# Building Scalable Microservices

Microservices architecture has become the de facto standard for building large-scale applications. Let's explore the key principles and patterns for successful microservices implementation.

## What Are Microservices?

Microservices are small, independent services that work together to form a complete application. Each service:

- Focuses on a single business capability
- Can be deployed independently
- Has its own database
- Communicates via well-defined APIs

## Key Principles

### 1. Single Responsibility

Each service should do one thing well:

```
❌ Bad: UserService handles users, orders, and payments
✅ Good: UserService, OrderService, PaymentService
```

### 2. Independent Deployment

Services should be deployable without affecting others:

```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: user-service
        image: user-service:v1.2.0
```

### 3. Decentralized Data Management

Each service owns its data:

```
Service A DB ← Service A
Service B DB ← Service B
Service C DB ← Service C
```

## Communication Patterns

### Synchronous (REST/gRPC)

```python
# REST with FastAPI
@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    # Call user service
    user = await http_client.get(f"http://user-service/users/{user_id}")
    return {"order": order, "user": user}
```

### Asynchronous (Message Queue)

```python
# RabbitMQ example
async def publish_order_created(order):
    await channel.basic_publish(
        exchange='orders',
        routing_key='order.created',
        body=json.dumps(order)
    )
```

## Service Discovery

Use service discovery for dynamic routing:

```python
# Consul integration
from consul import Consul

consul = Consul()
services = consul.health.service('user-service')[1]
service_url = f"http://{services[0]['Service']['Address']}:{services[0]['Service']['Port']}"
```

## API Gateway Pattern

Centralize client requests:

```
Client → API Gateway → Service A
                    → Service B
                    → Service C
```

## Circuit Breaker

Prevent cascading failures:

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_external_service():
    response = await http_client.get(external_url)
    return response
```

## Database Patterns

### Database per Service

Each service has its own database:

```
UserService → PostgreSQL
OrderService → MongoDB
PaymentService → PostgreSQL
```

### Event Sourcing

Store state changes as events:

```python
events = [
    {"type": "OrderCreated", "data": {...}},
    {"type": "OrderPaid", "data": {...}},
    {"type": "OrderShipped", "data": {...}}
]
```

## Monitoring and Observability

### Distributed Tracing

Use OpenTelemetry or Jaeger:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@app.get("/orders")
async def get_orders():
    with tracer.start_as_current_span("get_orders"):
        orders = await fetch_orders()
        return orders
```

### Centralized Logging

Use ELK stack or similar:

```python
import structlog

logger = structlog.get_logger()
logger.info("order.created", order_id=order.id, user_id=user.id)
```

## Deployment Strategies

### Blue-Green Deployment

```bash
# Deploy new version (green)
kubectl apply -f deployment-green.yaml

# Switch traffic
kubectl patch service myservice -p '{"spec":{"selector":{"version":"green"}}}'
```

### Canary Deployment

```yaml
# 90% to stable, 10% to canary
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
spec:
  http:
  - route:
    - destination:
        host: myservice
        subset: stable
      weight: 90
    - destination:
        host: myservice
        subset: canary
      weight: 10
```

## Security Best Practices

1. **Service-to-service authentication**: Use mutual TLS
2. **API Gateway authentication**: JWT tokens
3. **Secrets management**: Use Vault or similar
4. **Network policies**: Restrict service communication

## Challenges and Solutions

### Challenge: Distributed Transactions

Solution: Use Saga pattern:

```python
async def order_saga():
    try:
        await create_order()
        await reserve_inventory()
        await process_payment()
    except Exception:
        await compensate_inventory()
        await compensate_order()
```

### Challenge: Data Consistency

Solution: Use eventual consistency:

```python
# Publish event
await publish_event("order.created", order)

# Subscribe and update
@consumer.on("order.created")
async def update_inventory(order):
    await inventory_service.reserve(order.items)
```

## Conclusion

Building scalable microservices requires careful planning and the right patterns. Focus on:

- Clear service boundaries
- Robust communication patterns
- Comprehensive monitoring
- Automated deployment
- Resilience and fault tolerance

Start with a monolith, extract services gradually, and evolve your architecture based on real needs!""",
                "author_id": 2,
                "publication_date": datetime.now() - timedelta(days=14)
            }
        ]

        for post_data in posts_data:
            post = BlogPost(**post_data)
            db.add(post)

        db.commit()
        print(f"Created {len(posts_data)} blog posts")
        print("\nSeed completed successfully!")
        print(f"Total authors: {len(authors)}")
        print(f"Total posts: {len(posts_data)}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
