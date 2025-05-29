# Architecture Documentation

## Overview

The AI Chatbot application follows a modern microservices architecture with a clear separation between frontend, backend, and data layers. The system is designed for scalability, maintainability, and ease of deployment.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Databases     │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   PostgreSQL    │
│                 │    │                 │    │   ChromaDB      │
│   - UI/UX       │    │   - API         │    │   Redis         │
│   - State Mgmt  │    │   - Business    │    │                 │
│   - Routing     │    │   - Auth        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  External APIs  │
                       │   - OpenAI      │
                       │   - File System │
                       └─────────────────┘
```

## Component Architecture

### Frontend (React)

#### Component Hierarchy
```
App
├── AuthProvider (Context)
├── Router
│   ├── Login/Register (Public)
│   └── Layout (Private)
│       ├── Header
│       ├── Sidebar
│       └── Main Content
│           ├── Dashboard
│           ├── Chat
│           │   ├── SessionSidebar
│           │   ├── MessageList
│           │   └── ChatInput
│           └── Documents
│               ├── DocumentUpload
│               └── DocumentList
```

#### State Management
- **React Context**: Global authentication state
- **Local State**: Component-specific state
- **Services**: API communication layer

#### Key Features
- Responsive design with Tailwind CSS
- Real-time chat interface
- File upload with drag-and-drop
- Session management
- Error handling and notifications

### Backend (FastAPI)

#### Layered Architecture
```
┌─────────────────────────────────────────┐
│                Routers                  │
│  (auth, chat, documents, users)         │
├─────────────────────────────────────────┤
│               Services                  │
│  (auth, chat, document_processor)       │
├─────────────────────────────────────────┤
│                Models                   │
│  (database, schemas)                    │
├─────────────────────────────────────────┤
│                Utils                    │
│  (config, helpers)                      │
└─────────────────────────────────────────┘
```

#### Core Components

1. **Routers**: Handle HTTP requests and responses
2. **Services**: Business logic and external integrations
3. **Models**: Data models and validation schemas
4. **Utils**: Configuration and utility functions

#### Key Features
- JWT-based authentication
- Document processing with LangChain
- Vector embeddings with ChromaDB
- Real-time chat with WebSockets
- Background task processing
- Comprehensive error handling

## Data Architecture

### Database Schema

#### PostgreSQL (Primary Database)
```sql
Users
├── id (PK)
├── username (unique)
├── email (unique)
├── hashed_password
├── full_name
├── is_active
├── created_at
└── updated_at

Documents
├── id (PK)
├── filename
├── original_filename
├── file_path
├── file_size
├── content_type
├── processed
├── owner_id (FK → Users.id)
├── created_at
└── updated_at

ChatSessions
├── id (PK)
├── title
├── user_id (FK → Users.id)
├── created_at
└── updated_at

ChatMessages
├── id (PK)
├── session_id (FK → ChatSessions.id)
├── content
├── role (user/assistant)
└── timestamp
```

#### ChromaDB (Vector Database)
- **Collections**: Document embeddings
- **Metadata**: Document ID, chunk index, file path
- **Embeddings**: Sentence transformer vectors
- **Documents**: Text chunks for retrieval

#### Redis (Cache/Session Store)
- Session data
- Rate limiting counters
- Temporary file processing status

## Security Architecture

### Authentication Flow
```
1. User Login → JWT Token Generation
2. Token Storage → Local Storage (Frontend)
3. API Requests → Bearer Token in Headers
4. Token Validation → JWT Verification
5. User Context → Request Processing
```

### Security Measures
- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure token-based auth
- **CORS Configuration**: Restricted origins
- **Input Validation**: Pydantic schemas
- **File Upload Security**: Type and size validation
- **Rate Limiting**: Request throttling

## Document Processing Pipeline

```
File Upload
    ↓
File Validation
    ↓
File Storage
    ↓
Background Processing
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
Vector Storage (ChromaDB)
    ↓
Processing Complete
```

### Processing Steps
1. **Upload**: Secure file upload with validation
2. **Storage**: File system storage with unique names
3. **Extraction**: Text extraction (PDF, DOCX, TXT)
4. **Chunking**: Split text into manageable chunks
5. **Embedding**: Generate vector embeddings
6. **Indexing**: Store in ChromaDB for retrieval

## Chat Architecture

### Message Flow
```
User Input
    ↓
Session Management
    ↓
Document Retrieval (Optional)
    ↓
Context Preparation
    ↓
AI API Call
    ↓
Response Processing
    ↓
Message Storage
    ↓
UI Update
```

### Components
- **Session Management**: Organize conversations
- **Context Retrieval**: Find relevant documents
- **AI Integration**: OpenAI API calls
- **Fallback Handling**: Graceful degradation

## Deployment Architecture

### Development Environment
```
Dev Container
├── VS Code Extensions
├── Python Environment
├── Node.js Environment
└── Database Services
    ├── PostgreSQL
    ├── Redis
    └── ChromaDB
```

### Production Environment
```
Docker Compose
├── Frontend Container (Nginx)
├── Backend Container (FastAPI)
├── PostgreSQL Container
├── Redis Container
└── Volumes
    ├── Database Data
    ├── File Uploads
    └── Vector Database
```

## Scalability Considerations

### Horizontal Scaling
- **Frontend**: CDN distribution
- **Backend**: Load balancer + multiple instances
- **Database**: Read replicas
- **File Storage**: Object storage (S3)

### Performance Optimization
- **Caching**: Redis for frequent queries
- **Database Indexing**: Optimized queries
- **Connection Pooling**: Efficient DB connections
- **Background Tasks**: Async processing

## Monitoring and Observability

### Health Checks
- Application health endpoints
- Database connectivity
- External service availability

### Logging
- Structured logging with levels
- Request/response logging
- Error tracking and alerting

### Metrics
- Response times
- Error rates
- Resource utilization
- User activity

## Technology Decisions

### Backend Framework: FastAPI
**Reasons:**
- High performance (async support)
- Automatic API documentation
- Type hints and validation
- Modern Python features

### Frontend Framework: React
**Reasons:**
- Component-based architecture
- Large ecosystem
- TypeScript support
- Excellent developer tools

### Database: PostgreSQL
**Reasons:**
- ACID compliance
- JSON support
- Full-text search
- Mature and reliable

### Vector Database: ChromaDB
**Reasons:**
- Easy integration
- Local deployment
- Good performance
- Python-native

### Containerization: Docker
**Reasons:**
- Environment consistency
- Easy deployment
- Scalability
- Development efficiency

## Future Enhancements

### Planned Features
- Multi-language support
- Advanced document analysis
- Real-time collaboration
- Mobile application
- Advanced analytics

### Technical Improvements
- Microservices architecture
- Event-driven architecture
- Advanced caching strategies
- Machine learning pipelines
- Enhanced security measures
