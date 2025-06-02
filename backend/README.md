# Backend - Wellows AI Chatbot API

## Overview

The backend is a modern FastAPI application that provides a robust API for the Wellows AI chatbot system. It handles user authentication, document processing, AI-powered conversations, and data management.

## 🏗️ Architecture

```
backend/
├── app/                    # Main application package
│   ├── models/            # Data models and schemas
│   ├── routers/           # API route handlers
│   ├── services/          # Business logic layer
│   ├── utils/             # Utilities and configuration
│   └── main.py           # FastAPI application entry point
├── tests/                 # Unit and integration tests
├── requirements.txt       # Python dependencies
└── Dockerfile            # Container configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example .env
# Edit .env with your configuration

# Run the application
uvicorn app.main:app --reload
```

### Using Dev Container
```bash
# Open in VS Code with Remote-Containers extension
# The environment will be automatically configured
runapi  # Alias to start the API server
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/token` - User login
- `GET /api/auth/me` - Get current user

#### Chat
- `POST /api/chat/` - Send message and get AI response
- `GET /api/chat/sessions` - Get user's chat sessions
- `POST /api/chat/sessions` - Create new chat session

#### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - Get user's documents
- `DELETE /api/documents/{id}` - Delete document

#### Health
- `GET /health` - Health check endpoint

## 🔧 Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Redis
REDIS_URL=redis://localhost:6379

# File uploads
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
CHROMA_DB_PATH=chroma_db
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Structure
- `tests/conftest.py` - Test configuration and fixtures
- `tests/test_auth.py` - Authentication tests
- `tests/test_chat.py` - Chat functionality tests
- `tests/test_documents.py` - Document processing tests

## 📦 Dependencies

### Core Dependencies
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and settings
- **Uvicorn**: ASGI server
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage

### AI & Document Processing
- **OpenAI**: AI model integration
- **LangChain**: Document processing framework
- **ChromaDB**: Vector database for embeddings
- **pypdf**: PDF text extraction
- **python-docx**: Word document processing

### Security
- **python-jose**: JWT token handling
- **passlib**: Password hashing
- **python-multipart**: File upload support

## 🔒 Security

### Authentication
- JWT-based authentication
- Secure password hashing with bcrypt
- Token expiration and refresh

### Data Protection
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- File upload validation and sanitization
- CORS configuration for cross-origin requests

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Documents Table
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    content_type VARCHAR(100),
    processed BOOLEAN DEFAULT FALSE,
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t wellows-backend .

# Run container
docker run -p 8000:8000 --env-file .env wellows-backend
```

### Production Considerations
- Use environment-specific configuration
- Set up proper logging and monitoring
- Configure reverse proxy (nginx)
- Set up SSL/TLS certificates
- Use production-grade database
- Implement rate limiting
- Set up backup strategies

## 🔍 Monitoring & Logging

### Health Checks
- `/health` endpoint for basic health monitoring
- Database connectivity checks
- External service availability checks

### Logging
- Structured logging with Python's logging module
- Request/response logging
- Error tracking and alerting
- Performance metrics

## 🤝 Contributing

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Use isort for import sorting
- Type hints for all functions
- Comprehensive docstrings

### Development Workflow
1. Create feature branch
2. Write tests for new functionality
3. Implement the feature
4. Run tests and linting
5. Submit pull request

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📈 Performance

### Optimization Strategies
- Database query optimization
- Connection pooling
- Caching with Redis
- Async/await for I/O operations
- Background task processing
- Response compression

### Monitoring
- Response time tracking
- Database query performance
- Memory usage monitoring
- Error rate tracking

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database status
pg_isready -h localhost -p 5432

# Check connection string
echo $DATABASE_URL
```

#### Import Errors
```bash
# Ensure virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt
```

#### OpenAI API Errors
- Verify API key is set correctly
- Check API quota and billing
- Application provides fallback responses

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug

# Enable debug mode in settings
export DEBUG=true
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
