#!/usr/bin/env python3
"""
Basic test to verify the application structure.
"""

import sys
import os

def test_backend_structure():
    """Test that backend files exist."""
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/models/database.py',
        'app/services/auth.py',
        'app/routers/auth.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing backend files: {missing_files}")
        return False
    
    print("✅ Backend structure is complete")
    return True

def test_frontend_structure():
    """Test that frontend files exist."""
    frontend_path = '../frontend'
    required_files = [
        'package.json',
        'src/App.tsx',
        'src/index.tsx',
        'src/components/Auth/Login.tsx',
        'src/services/api.ts'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(frontend_path, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing frontend files: {missing_files}")
        return False
    
    print("✅ Frontend structure is complete")
    return True

def test_docker_files():
    """Test that Docker files exist."""
    required_files = [
        'Dockerfile',
        '../docker-compose.yml',
        '../.devcontainer/devcontainer.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing Docker files: {missing_files}")
        return False
    
    print("✅ Docker configuration is complete")
    return True

def test_documentation():
    """Test that documentation exists."""
    required_files = [
        '../README.md',
        '../docs/API.md',
        '../docs/SETUP.md',
        '../docs/ARCHITECTURE.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing documentation files: {missing_files}")
        return False
    
    print("✅ Documentation is complete")
    return True

def main():
    """Run all tests."""
    print("🧪 Testing AI Chatbot Application Structure\n")
    
    tests = [
        test_backend_structure,
        test_frontend_structure,
        test_docker_files,
        test_documentation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application structure is complete.")
        return 0
    else:
        print("❌ Some tests failed. Please check the missing files.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
