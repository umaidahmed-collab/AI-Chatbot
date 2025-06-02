#!/bin/bash

set -e

echo "🗄️ Setting up database for Wellows..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if PostgreSQL is running
if ! pg_isready -h postgres -p 5432 -U chatbot >/dev/null 2>&1; then
    print_error "PostgreSQL is not running. Please start the database service first."
    echo "Run: docker-compose up postgres"
    exit 1
fi

print_status "PostgreSQL is running"

# Run database migrations/setup
cd /workspace/backend

if [ -f "app/services/database.py" ]; then
    print_status "Initializing database tables..."
    python -c "
import asyncio
from app.services.database import init_db
asyncio.run(init_db())
print('Database initialized successfully!')
"
    print_success "Database setup complete"
else
    print_error "Database initialization script not found"
    exit 1
fi

print_success "🎉 Database setup completed successfully!"
