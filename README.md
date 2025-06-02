# Wellows AI Chatbot

A comprehensive AI chatbot application with advanced document processing capabilities. Built with modern technologies and designed for scalability, security, and developer productivity.

## ✨ Features

### 🤖 **AI-Powered Conversations**
- Intelligent conversations using OpenAI GPT models
- Context-aware responses with document integration
- Fallback responses when API is unavailable
- Conversation history and session management

### 📄 **Advanced Document Processing**
- Support for PDF, DOCX, and TXT files
- Automatic text extraction and chunking
- OpenAI embeddings for semantic search
- Vector database storage with ChromaDB
- Real-time processing status updates

### 🔐 **Enterprise-Grade Security**
- JWT-based authentication system
- Secure password hashing with bcrypt
- Input validation and sanitization
- CORS configuration and rate limiting
- File upload security and validation

### 💻 **Modern Development Experience**
- Complete dev container setup with VS Code
- Hot reload for both frontend and backend
- Comprehensive testing suites
- Code formatting and linting
- Pre-commit hooks and CI/CD ready

### 📱 **Responsive User Interface**
- Modern React with TypeScript
- Tailwind CSS for consistent styling
- Drag-and-drop file uploads
- Real-time chat interface
- Mobile-optimized design

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
```

### Frontend Tests
```bash
cd frontend
npm test
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

## Configuration

### Environment Variables

#### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI responses
- `SECRET_KEY`: JWT secret key
- `REDIS_URL`: Redis connection string

#### Frontend
- `REACT_APP_API_URL`: Backend API URL

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

## 📚 Enhanced Documentation

This project includes comprehensive documentation for all components:

### 📁 **Folder-Level Documentation**
- **[Backend Documentation](./backend/README.md)** - Complete backend API guide
- **[Frontend Documentation](./frontend/README.md)** - React application guide
- **[Dev Container Documentation](./.devcontainer/README.md)** - Development environment setup
- **[Tests Documentation](./backend/tests/README.md)** - Testing strategies and guidelines
- **[Docs Overview](./docs/README.md)** - Documentation structure and standards

### 🔧 **Development Guides**
- **[API Reference](./docs/API.md)** - Complete API documentation
- **[Setup Guide](./docs/SETUP.md)** - Installation and configuration
- **[Architecture Overview](./docs/ARCHITECTURE.md)** - System design and components

### 🚀 **Quick Development Commands**

When using the dev container, you have access to convenient aliases:

```bash
# Navigation
backend     # Navigate to backend directory
frontend    # Navigate to frontend directory
docs        # Navigate to docs directory

# Development
runapi      # Start backend API server
runfrontend # Start frontend development server

# Testing
test-backend   # Run backend tests with coverage
test-frontend  # Run frontend tests

# Code Quality
lint        # Run linting on both backend and frontend
format      # Format code in both backend and frontend

# Docker
dcup        # docker-compose up
dcdown      # docker-compose down
dclogs      # docker-compose logs -f
```

## 🎯 **LAB Tasks Completed**

This implementation addresses the following JIRA tickets:

### ✅ **LAB-10: Setup a .devcontainer**
- Complete VS Code dev container configuration
- Multi-language support (Python + Node.js)
- Pre-configured extensions and settings
- Automated setup scripts
- Database and service integration
- Convenient development aliases

### ✅ **LAB-2: Generate markdown documentation**
- Comprehensive README for each folder
- API documentation with examples
- Setup and deployment guides
- Architecture documentation
- Testing guidelines and best practices
- Development workflow documentation

## 🔄 **Next Steps**

Ready for additional LAB tasks:
- **LAB-8**: Unit testing plan (foundation already in place)
- **LAB-11**: AI IDE guidelines (dev container provides foundation)
- **LAB-12**: PRD and TDD documentation
- **LAB-16**: Documentation website compilation
