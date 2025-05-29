# Setup Guide

This guide will help you set up the AI Chatbot application for development and production.

## Prerequisites

### Required Software
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository
- **VS Code**: Recommended for development (with Remote-Containers extension)

### Optional
- **Node.js**: Version 18+ (for local frontend development)
- **Python**: Version 3.11+ (for local backend development)
- **PostgreSQL**: Version 15+ (for local database)

## Development Setup

### Option 1: Dev Containers (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AI-Made-BOT
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Install Remote-Containers extension:**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Remote - Containers"
   - Install the extension

4. **Reopen in container:**
   - Press `Ctrl+Shift+P`
   - Type "Remote-Containers: Reopen in Container"
   - Select the command
   - Wait for the container to build and start

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

6. **Start the services:**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API keys
   ```

5. **Start PostgreSQL and Redis:**
   ```bash
   docker-compose up postgres redis
   ```

6. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

## Production Setup

### Docker Compose Deployment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AI-Made-BOT
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Build and start services:**
   ```bash
   docker-compose up --build -d
   ```

4. **Verify deployment:**
   ```bash
   docker-compose ps
   docker-compose logs
   ```

### Manual Production Setup

#### Backend Production

1. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set up database:**
   ```bash
   # Install PostgreSQL
   sudo apt-get install postgresql postgresql-contrib
   
   # Create database and user
   sudo -u postgres psql
   CREATE DATABASE chatbot_db;
   CREATE USER chatbot WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot;
   ```

3. **Set up Redis:**
   ```bash
   sudo apt-get install redis-server
   sudo systemctl start redis-server
   ```

4. **Configure environment:**
   ```bash
   export DATABASE_URL="postgresql://chatbot:password@localhost/chatbot_db"
   export OPENAI_API_KEY="your_openai_key"
   export SECRET_KEY="your_secret_key"
   ```

5. **Run with Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

#### Frontend Production

1. **Build the application:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Serve with Nginx:**
   ```bash
   sudo apt-get install nginx
   sudo cp nginx.conf /etc/nginx/sites-available/chatbot
   sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

## Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://chatbot:password@localhost:5432/chatbot_db

# Security
SECRET_KEY=your-super-secret-key-change-in-production
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

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## Database Migration

The application automatically creates database tables on startup. For manual migration:

```bash
cd backend
python -c "from app.services.database import init_db; import asyncio; asyncio.run(init_db())"
```

## Testing

### Run Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Run Frontend Tests
```bash
cd frontend
npm test
npm test -- --coverage  # With coverage
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using the port
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Database connection error:**
   - Verify PostgreSQL is running
   - Check DATABASE_URL format
   - Ensure database exists

3. **OpenAI API errors:**
   - Verify API key is correct
   - Check API quota and billing
   - Application works without API key (fallback responses)

4. **File upload issues:**
   - Check file permissions on upload directory
   - Verify file size limits
   - Ensure supported file types

5. **Docker issues:**
   ```bash
   # Clean up Docker
   docker-compose down -v
   docker system prune -a
   
   # Rebuild containers
   docker-compose up --build
   ```

### Logs

#### View application logs:
```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# Local development
# Backend logs are in the terminal
# Frontend logs are in the browser console
```

#### Enable debug mode:
```bash
# Backend
export DEBUG=True

# Frontend
export REACT_APP_DEBUG=true
```

## Performance Optimization

### Backend
- Use Redis for caching
- Configure database connection pooling
- Enable gzip compression
- Use CDN for static files

### Frontend
- Enable production build optimizations
- Use lazy loading for components
- Implement proper caching headers
- Optimize images and assets

## Security Considerations

1. **Change default passwords**
2. **Use strong SECRET_KEY**
3. **Enable HTTPS in production**
4. **Configure CORS properly**
5. **Implement rate limiting**
6. **Regular security updates**
7. **Monitor for vulnerabilities**

## Monitoring

### Health Checks
- Backend: `GET /health`
- Database: Check connection status
- Redis: Check connection status

### Metrics
- Response times
- Error rates
- Database performance
- File upload success rates

## Backup

### Database Backup
```bash
pg_dump chatbot_db > backup.sql
```

### File Backup
```bash
tar -czf uploads_backup.tar.gz uploads/
tar -czf chroma_backup.tar.gz chroma_db/
```
