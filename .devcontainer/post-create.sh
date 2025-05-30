#!/bin/bash

set -e

echo "🚀 Setting up Wellows development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Update system packages
print_status "Updating system packages..."
sudo apt-get update -qq

# Install additional development tools
print_status "Installing additional development tools..."
sudo apt-get install -y -qq \
    tree \
    htop \
    jq \
    curl \
    wget \
    unzip \
    zip \
    make \
    build-essential

# Set up Git configuration
print_status "Setting up Git configuration..."
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf input

# Install backend dependencies
print_status "Installing backend dependencies..."
cd /workspace/backend
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Backend dependencies installed"
else
    print_warning "No requirements.txt found in backend directory"
fi

# Install development dependencies
if [ -f "/workspace/.devcontainer/requirements.dev.txt" ]; then
    print_status "Installing development dependencies..."
    pip install -r /workspace/.devcontainer/requirements.dev.txt
    print_success "Development dependencies installed"
fi

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd /workspace/frontend
if [ -f "package.json" ]; then
    npm install
    print_success "Frontend dependencies installed"
else
    print_warning "No package.json found in frontend directory"
fi

# Set up pre-commit hooks
cd /workspace
if [ -f ".pre-commit-config.yaml" ]; then
    print_status "Setting up pre-commit hooks..."
    pre-commit install
    print_success "Pre-commit hooks installed"
else
    print_warning "No .pre-commit-config.yaml found"
fi

# Create useful aliases
print_status "Setting up shell aliases..."
cat >> ~/.bashrc << 'EOF'

# Wellows Development Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Project specific aliases
alias backend='cd /workspace/backend'
alias frontend='cd /workspace/frontend'
alias docs='cd /workspace/docs'
alias runapi='cd /workspace/backend && uvicorn app.main:app --reload --host 0.0.0.0'
alias runfrontend='cd /workspace/frontend && npm start'
alias test-backend='cd /workspace/backend && pytest'
alias test-frontend='cd /workspace/frontend && npm test'
alias lint='cd /workspace/backend && pylint app/ && cd /workspace/frontend && npm run lint'
alias format='cd /workspace/backend && black app/ && isort app/ && cd /workspace/frontend && npm run format'

# Docker aliases
alias dc='docker-compose'
alias dcup='docker-compose up'
alias dcdown='docker-compose down'
alias dcbuild='docker-compose build'
alias dclogs='docker-compose logs -f'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gb='git branch'
alias gco='git checkout'
alias gd='git diff'
alias glog='git log --oneline --graph --decorate'
EOF

# Set up environment variables
print_status "Setting up environment variables..."
if [ ! -f "/workspace/.env" ] && [ -f "/workspace/.env.example" ]; then
    cp /workspace/.env.example /workspace/.env
    print_success "Environment file created from template"
fi

# Create useful directories
print_status "Creating project directories..."
mkdir -p /workspace/{logs,temp,uploads,chroma_db}

# Set proper permissions
print_status "Setting permissions..."
sudo chown -R vscode:vscode /workspace
chmod +x /workspace/.devcontainer/scripts/*.sh 2>/dev/null || true

print_success "🎉 Wellows development environment setup complete!"
print_status "Available commands:"
echo "  - runapi: Start the backend API server"
echo "  - runfrontend: Start the frontend development server"
echo "  - test-backend: Run backend tests"
echo "  - test-frontend: Run frontend tests"
echo "  - lint: Run linting on both backend and frontend"
echo "  - format: Format code in both backend and frontend"
echo ""
print_status "To get started:"
echo "  1. Copy .env.example to .env and configure your settings"
echo "  2. Run 'runapi' to start the backend"
echo "  3. Run 'runfrontend' to start the frontend"
echo ""
print_status "Happy coding! 🚀"
