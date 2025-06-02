# Backend Tests - Wellows AI Chatbot

## Overview

This directory contains comprehensive test suites for the Wellows AI Chatbot backend. The tests ensure code quality, functionality, and reliability across all components of the application.

## 🏗️ Test Structure

```
tests/
├── README.md              # This documentation
├── conftest.py           # Test configuration and fixtures
├── test_auth.py          # Authentication tests
├── test_chat.py          # Chat functionality tests
├── test_documents.py     # Document processing tests
├── test_users.py         # User management tests
├── test_api.py           # API endpoint tests
├── integration/          # Integration tests
│   ├── test_full_flow.py # End-to-end workflow tests
│   └── test_database.py  # Database integration tests
├── unit/                 # Unit tests
│   ├── test_services.py  # Service layer tests
│   ├── test_models.py    # Model validation tests
│   └── test_utils.py     # Utility function tests
└── fixtures/             # Test data and fixtures
    ├── sample_documents/ # Sample files for testing
    └── test_data.json    # Test data sets
```

## 🚀 Running Tests

### Quick Start
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_login"
```

### Using Dev Container
```bash
# Use the convenient alias
test-backend

# Or use the comprehensive test script
.devcontainer/scripts/run-tests.sh --backend-only
```

## 🧪 Test Categories

### Unit Tests
Test individual components in isolation:
- **Models**: Data validation and serialization
- **Services**: Business logic and external integrations
- **Utils**: Helper functions and utilities
- **Routers**: Request/response handling

### Integration Tests
Test component interactions:
- **Database**: ORM operations and queries
- **API**: Full request/response cycles
- **External Services**: OpenAI, ChromaDB integrations
- **File Processing**: Document upload and processing

### End-to-End Tests
Test complete user workflows:
- **User Registration**: Account creation flow
- **Document Upload**: File processing pipeline
- **Chat Conversations**: Complete chat interactions
- **Authentication**: Login/logout flows

## 🔧 Test Configuration

### conftest.py
Central test configuration providing:
- **Test Database**: Isolated SQLite database
- **Test Client**: FastAPI test client
- **Fixtures**: Reusable test data and objects
- **Mocks**: External service mocking

### Key Fixtures
```python
@pytest.fixture
def client():
    """Test client for API requests."""
    
@pytest.fixture
def db():
    """Test database session."""
    
@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    
@pytest.fixture
def authenticated_client(client, test_user_data):
    """Client with authenticated user."""
```

## 📊 Test Coverage

### Coverage Goals
- **Overall Coverage**: > 90%
- **Critical Paths**: 100% (auth, payments, data processing)
- **Business Logic**: > 95%
- **API Endpoints**: 100%

### Coverage Reports
```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# View report
open htmlcov/index.html

# Terminal coverage report
pytest --cov=app --cov-report=term-missing
```

### Coverage Configuration
```ini
# .coveragerc
[run]
source = app
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 🎯 Test Examples

### Authentication Tests
```python
def test_register_user(client, test_user_data):
    """Test user registration."""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert "id" in data

def test_login_user(client, test_user_data):
    """Test user login."""
    # Register user first
    client.post("/api/auth/register", json=test_user_data)
    
    # Login
    response = client.post(
        "/api/auth/token",
        data={"username": test_user_data["username"], 
              "password": test_user_data["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
```

### Chat Tests
```python
def test_send_chat_message(authenticated_client):
    """Test sending a chat message."""
    message_data = {
        "message": "Hello, how are you?",
        "use_documents": False
    }
    response = authenticated_client.post("/api/chat/", json=message_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "session_id" in data
```

### Document Tests
```python
def test_upload_document(authenticated_client):
    """Test document upload."""
    with open("tests/fixtures/sample.pdf", "rb") as f:
        response = authenticated_client.post(
            "/api/documents/upload",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["original_filename"] == "sample.pdf"
```

## 🔍 Testing Best Practices

### Test Organization
- **One test per function**: Each test should verify one specific behavior
- **Descriptive names**: Test names should clearly describe what they test
- **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
- **Independent tests**: Tests should not depend on each other

### Test Data Management
```python
# Use factories for test data
@pytest.fixture
def user_factory():
    def _create_user(**kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        defaults.update(kwargs)
        return defaults
    return _create_user

# Use parametrized tests for multiple scenarios
@pytest.mark.parametrize("username,email,expected_status", [
    ("validuser", "valid@email.com", 200),
    ("", "valid@email.com", 422),
    ("validuser", "invalid-email", 422),
])
def test_user_registration_validation(client, username, email, expected_status):
    response = client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": "validpass123"
    })
    assert response.status_code == expected_status
```

### Mocking External Services
```python
@pytest.fixture
def mock_openai():
    with patch('app.services.chat_service.openai') as mock:
        mock.ChatCompletion.create.return_value = {
            "choices": [{"message": {"content": "Mocked response"}}]
        }
        yield mock

def test_chat_with_mocked_openai(authenticated_client, mock_openai):
    """Test chat with mocked OpenAI response."""
    response = authenticated_client.post("/api/chat/", json={
        "message": "Test message",
        "use_documents": False
    })
    assert response.status_code == 200
    assert "Mocked response" in response.json()["message"]
```

## 🚨 Error Testing

### Exception Handling
```python
def test_invalid_login_credentials(client):
    """Test login with invalid credentials."""
    response = client.post("/api/auth/token", data={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_unauthorized_access(client):
    """Test accessing protected endpoint without authentication."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401
```

### Validation Testing
```python
def test_invalid_file_upload(authenticated_client):
    """Test uploading invalid file type."""
    response = authenticated_client.post(
        "/api/documents/upload",
        files={"file": ("test.exe", b"fake content", "application/exe")}
    )
    assert response.status_code == 400
    assert "File type" in response.json()["detail"]
```

## 🔄 Continuous Integration

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [backend/tests/]
```

## 📈 Performance Testing

### Load Testing
```python
import asyncio
import aiohttp
import time

async def test_api_performance():
    """Test API response times under load."""
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        tasks = []
        
        for _ in range(100):
            task = session.get("http://localhost:8000/health")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        assert all(r.status == 200 for r in responses)
        assert (end_time - start_time) < 5.0  # Should complete in under 5 seconds
```

## 🔧 Debugging Tests

### Running Specific Tests
```bash
# Run single test
pytest tests/test_auth.py::test_login_user -v

# Run tests with debugging
pytest tests/test_auth.py::test_login_user -v -s --pdb

# Run failed tests only
pytest --lf

# Run tests with specific markers
pytest -m "slow" -v
```

### Test Debugging Tips
- Use `pytest.set_trace()` for debugging
- Add `print()` statements for debugging (use `-s` flag)
- Use `--pdb` flag to drop into debugger on failures
- Check test database state with database fixtures

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

## 🤝 Contributing Tests

### Adding New Tests
1. **Identify test cases**: What scenarios need testing?
2. **Choose test type**: Unit, integration, or end-to-end?
3. **Write test**: Follow existing patterns and conventions
4. **Run tests**: Ensure new tests pass and don't break existing ones
5. **Update coverage**: Aim to maintain or improve coverage

### Test Review Checklist
- [ ] Test names are descriptive
- [ ] Tests are independent and isolated
- [ ] Edge cases are covered
- [ ] Error conditions are tested
- [ ] Mocks are used appropriately
- [ ] Test data is realistic
- [ ] Coverage is maintained or improved
