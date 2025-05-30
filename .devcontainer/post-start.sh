#!/bin/bash

set -e

echo "🔄 Running post-start setup for Wellows..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Wait for services to be ready
print_status "Waiting for services to be ready..."

# Wait for PostgreSQL
print_status "Checking PostgreSQL connection..."
for i in {1..30}; do
    if pg_isready -h postgres -p 5432 -U chatbot >/dev/null 2>&1; then
        print_success "PostgreSQL is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "PostgreSQL is not ready after 30 attempts"
    fi
    sleep 1
done

# Wait for Redis
print_status "Checking Redis connection..."
for i in {1..30}; do
    if redis-cli -h redis ping >/dev/null 2>&1; then
        print_success "Redis is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Redis is not ready after 30 attempts"
    fi
    sleep 1
done

# Source the aliases
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Display helpful information
print_status "🎯 Wellows Development Environment Ready!"
echo ""
echo "📊 Service Status:"
echo "  - PostgreSQL: Available on port 5432"
echo "  - Redis: Available on port 6379"
echo "  - Backend API: Ready to start on port 8000"
echo "  - Frontend: Ready to start on port 3000"
echo ""
echo "🚀 Quick Start Commands:"
echo "  - runapi      # Start backend API"
echo "  - runfrontend # Start frontend"
echo "  - test-backend # Run backend tests"
echo "  - gs          # Git status"
echo "  - dcup        # Start all services with Docker Compose"
echo ""
echo "📁 Project Structure:"
tree -L 2 /workspace -I 'node_modules|__pycache__|.git' 2>/dev/null || echo "  Use 'tree' command to explore the project structure"
echo ""

print_success "Ready for development! 🚀"
