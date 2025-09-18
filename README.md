# AI Chatbot with Document Upload

A complete chatbot application with document upload and processing capabilities. Built with FastAPI backend, React frontend, and AI-powered conversations using uploaded documents.

## Features

- 🤖 **AI-Powered Chat**: Intelligent conversations using OpenAI GPT models
- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 🔍 **Document Search**: AI can reference uploaded documents in conversations
- 💬 **Chat Sessions**: Organize conversations into sessions
- 🔐 **User Authentication**: Secure login and registration
- 📱 **Responsive UI**: Modern, mobile-friendly interface
- 🐳 **Containerized**: Full Docker support with dev containers
- 🧪 **Tested**: Comprehensive unit tests for backend and frontend

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Primary database
- **ChromaDB**: Vector database for document embeddings
- **LangChain**: Document processing and AI integration
- **Redis**: Caching and session storage

### Frontend
- **React**: UI framework with TypeScript
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Router**: Client-side routing

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Dev Containers**: Development environment

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key (optional, fallback responses available)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-Made-BOT
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. Run with Docker Compose
```bash
# Development
docker-compose -f docker-compose.dev.yml up --build

# Production
docker-compose up --build
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Setup

### Using Dev Containers (Recommended)
1. Open the project in VS Code
2. Install the "Remote - Containers" extension
3. Press `Ctrl+Shift+P` and select "Remote-Containers: Reopen in Container"
4. The development environment will be automatically set up

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login and get access token
- `GET /api/auth/me` - Get current user info

#### Chat
- `POST /api/chat/` - Send message and get AI response
- `GET /api/chat/sessions` - Get user's chat sessions
- `POST /api/chat/sessions` - Create new chat session

#### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - Get user's documents
- `DELETE /api/documents/{id}` - Delete document

## Testing

### Backend Tests
```bash
cd backend
pytest

# Run with coverage
pytest --cov=app

# Run specific test modules
pytest tests/test_chat.py
pytest tests/test_chat_service.py

# Run with verbose output
pytest -v
```

### Frontend Tests
```bash
cd frontend
npm test

# Run tests in watch mode
npm test -- --watchAll

# Run with coverage
npm test -- --coverage
```

### Basic Structure Test
```bash
# Verify application structure
python test_basic.py
```

### Integration Testing
```bash
# Test full application with Docker
docker-compose -f docker-compose.dev.yml up --build

# Run end-to-end tests
cd frontend && npm run test:e2e  # If available
```

### Test Examples

#### Testing Chat Functionality
The application includes comprehensive test cases for chat functionality:

- **Chat Service Tests**: `backend/tests/test_chat_service.py`
  - Session creation and management
  - Message handling with conversation history
  - OpenAI API integration testing
  - Document context retrieval
  - Error handling and fallback responses

- **Chat API Tests**: `backend/tests/test_chat.py`
  - API endpoint testing
  - Authentication validation
  - Request/response validation
  - Error response handling

#### Running Specific Test Scenarios
```bash
# Test OpenAI integration (with mocking)
pytest backend/tests/test_chat_service.py::TestChatService::test_get_ai_response_success

# Test conversation history handling
pytest backend/tests/test_chat_service.py::TestChatService::test_chat_with_session_and_context

# Test error handling
pytest backend/tests/test_chat_service.py::TestChatService::test_get_ai_response_error
```

## Project Structure

```
AI-Made-BOT/
├── .devcontainer/          # Dev container configuration
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── models/         # Database models and schemas
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities and configuration
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript types
│   └── package.json        # Node.js dependencies
├── docs/                   # Documentation
├── docker-compose.yml      # Production compose
├── docker-compose.dev.yml  # Development compose
└── README.md
```

## Recent Bug Fixes

### OpenAI API Integration (Fixed in v1.2)
**Issue**: Outdated OpenAI library usage causing API call failures
- **Problem**: Using deprecated `openai.ChatCompletion.acreate()` method
- **Solution**: Updated to new `AsyncOpenAI` client with `chat.completions.create()`
- **Files Modified**: `backend/app/services/chat_service.py`, `backend/requirements.txt`
- **Impact**: Restored AI chat functionality with proper async OpenAI integration

### Conversation History Handling (Fixed in v1.2.1)
**Issue**: Duplicate user messages and incorrect conversation flow
- **Problem**: User message was added to database before retrieving conversation history
- **Solution**: Reordered operations to get history first, then add both user and AI messages
- **Files Modified**: `backend/app/services/chat_service.py`
- **Impact**: Fixed conversation context and message ordering

### Test Coverage Enhancement (v1.2.2)
**Enhancement**: Added comprehensive test suite for chat functionality
- **Added**: 305+ test cases covering chat API endpoints
- **Added**: 353+ test cases for chat service business logic
- **Files Added**: Enhanced `backend/tests/test_chat.py` and `backend/tests/test_chat_service.py`
- **Coverage**: Chat service, OpenAI integration, error handling, conversation management

## Troubleshooting

### Common Issues

#### OpenAI API Key Issues
**Symptoms**: Chat responses showing fallback messages or "Unable to get AI response"
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Verify API key in Docker
docker-compose exec backend env | grep OPENAI
```
**Solutions**:
- Ensure `.env` file contains valid `OPENAI_API_KEY=sk-...`
- Restart services after adding API key: `docker-compose restart`
- Check OpenAI API key validity at https://platform.openai.com/api-keys

#### Database Connection Issues
**Symptoms**: Backend fails to start with database errors
```bash
# Check database connectivity
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up --build
```

#### Frontend API Connection Issues
**Symptoms**: Frontend can't connect to backend API
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify frontend environment
docker-compose exec frontend env | grep REACT_APP_API_URL
```
**Solutions**:
- Ensure `REACT_APP_API_URL=http://localhost:8000` in frontend environment
- Check CORS settings in backend
- Verify both services are on same Docker network

#### Document Upload Failures
**Symptoms**: Document uploads fail or don't process
```bash
# Check ChromaDB connectivity
docker-compose logs chromadb

# Verify file permissions
ls -la uploads/
```
**Solutions**:
- Ensure uploads directory has write permissions
- Check file size limits (default: 10MB)
- Verify supported file types: PDF, DOCX, TXT

#### Memory Issues During Development
**Symptoms**: Services crashing or slow performance
```bash
# Monitor resource usage
docker stats

# Clean up unused containers/images
docker system prune
```

### Development Issues

#### Hot Reload Not Working
```bash
# Frontend hot reload
cd frontend && npm start

# Backend hot reload (development)
cd backend && uvicorn app.main:app --reload --host 0.0.0.0
```

#### Test Failures
```bash
# Clear test cache
cd backend && python -m pytest --cache-clear

# Run tests with detailed output
pytest -v -s

# Check test database
pytest --setup-show
```

#### Docker Build Failures
```bash
# Clean build
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check build logs
docker-compose logs --tail=50
```

### Performance Optimization

#### Database Performance
```bash
# Check database connections
docker-compose exec postgres psql -U postgres -c "SELECT * FROM pg_stat_activity;"

# Optimize database (if needed)
docker-compose exec postgres psql -U postgres -c "VACUUM ANALYZE;"
```

#### Redis Cache Issues
```bash
# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL

# Monitor Redis
docker-compose exec redis redis-cli MONITOR
```

## Configuration

### Environment Variables

#### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI responses (optional, fallback responses available)
- `SECRET_KEY`: JWT secret key for authentication
- `REDIS_URL`: Redis connection string for caching

#### Frontend
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

## Deployment

### Docker Deployment
```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment-Specific Deployment
- Development: Use `docker-compose.dev.yml`
- Production: Use `docker-compose.yml`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `docs/` folder
- Review the API documentation at `/docs` endpoint
