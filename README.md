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
