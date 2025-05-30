#!/bin/bash

set -e

echo "🧪 Running comprehensive tests for Wellows..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to run backend tests
run_backend_tests() {
    print_status "Running backend tests..."
    cd /workspace/backend
    
    if [ -f "requirements.txt" ]; then
        # Run pytest with coverage
        if command -v pytest >/dev/null 2>&1; then
            pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
            print_success "Backend tests completed"
        else
            print_warning "pytest not found, skipping backend tests"
        fi
    else
        print_warning "Backend requirements.txt not found, skipping backend tests"
    fi
}

# Function to run frontend tests
run_frontend_tests() {
    print_status "Running frontend tests..."
    cd /workspace/frontend
    
    if [ -f "package.json" ]; then
        if npm list --depth=0 | grep -q "react-scripts"; then
            npm test -- --coverage --watchAll=false
            print_success "Frontend tests completed"
        else
            print_warning "react-scripts not found, skipping frontend tests"
        fi
    else
        print_warning "Frontend package.json not found, skipping frontend tests"
    fi
}

# Function to run linting
run_linting() {
    print_status "Running code linting..."
    
    # Backend linting
    cd /workspace/backend
    if command -v pylint >/dev/null 2>&1; then
        pylint app/ --exit-zero
        print_success "Backend linting completed"
    else
        print_warning "pylint not found, skipping backend linting"
    fi
    
    # Frontend linting
    cd /workspace/frontend
    if [ -f "package.json" ] && npm list --depth=0 | grep -q "eslint"; then
        npm run lint --if-present
        print_success "Frontend linting completed"
    else
        print_warning "ESLint not configured, skipping frontend linting"
    fi
}

# Function to run type checking
run_type_checking() {
    print_status "Running type checking..."
    
    # Backend type checking
    cd /workspace/backend
    if command -v mypy >/dev/null 2>&1; then
        mypy app/ --ignore-missing-imports
        print_success "Backend type checking completed"
    else
        print_warning "mypy not found, skipping backend type checking"
    fi
    
    # Frontend type checking
    cd /workspace/frontend
    if [ -f "tsconfig.json" ]; then
        npx tsc --noEmit --skipLibCheck
        print_success "Frontend type checking completed"
    else
        print_warning "TypeScript config not found, skipping frontend type checking"
    fi
}

# Main execution
echo "🚀 Starting comprehensive test suite..."
echo ""

# Parse command line arguments
BACKEND_TESTS=true
FRONTEND_TESTS=true
LINTING=true
TYPE_CHECKING=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            FRONTEND_TESTS=false
            LINTING=false
            TYPE_CHECKING=false
            shift
            ;;
        --frontend-only)
            BACKEND_TESTS=false
            LINTING=false
            TYPE_CHECKING=false
            shift
            ;;
        --no-lint)
            LINTING=false
            shift
            ;;
        --no-types)
            TYPE_CHECKING=false
            shift
            ;;
        *)
            echo "Unknown option $1"
            echo "Usage: $0 [--backend-only] [--frontend-only] [--no-lint] [--no-types]"
            exit 1
            ;;
    esac
done

# Run tests based on flags
if [ "$BACKEND_TESTS" = true ]; then
    run_backend_tests
    echo ""
fi

if [ "$FRONTEND_TESTS" = true ]; then
    run_frontend_tests
    echo ""
fi

if [ "$LINTING" = true ]; then
    run_linting
    echo ""
fi

if [ "$TYPE_CHECKING" = true ]; then
    run_type_checking
    echo ""
fi

print_success "🎉 All tests completed!"
echo ""
echo "📊 Test Results Summary:"
echo "  - Backend Tests: $([ "$BACKEND_TESTS" = true ] && echo "✅ Run" || echo "⏭️ Skipped")"
echo "  - Frontend Tests: $([ "$FRONTEND_TESTS" = true ] && echo "✅ Run" || echo "⏭️ Skipped")"
echo "  - Code Linting: $([ "$LINTING" = true ] && echo "✅ Run" || echo "⏭️ Skipped")"
echo "  - Type Checking: $([ "$TYPE_CHECKING" = true ] && echo "✅ Run" || echo "⏭️ Skipped")"
echo ""
echo "📁 Coverage reports (if generated):"
echo "  - Backend: /workspace/backend/htmlcov/index.html"
echo "  - Frontend: /workspace/frontend/coverage/lcov-report/index.html"
