#!/bin/bash

echo "Setting up development environment..."

# Install backend dependencies
cd /workspace/backend
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Install frontend dependencies
cd /workspace/frontend
if [ -f "package.json" ]; then
    npm install
fi

# Set up pre-commit hooks
cd /workspace
if [ -f ".pre-commit-config.yaml" ]; then
    pre-commit install
fi

echo "Development environment setup complete!"
