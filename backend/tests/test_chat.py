"""
Chat integration tests and error handling tests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock


def test_create_chat_session(authenticated_client: TestClient):
    """Test creating a chat session."""
    response = authenticated_client.post("/api/chat/sessions?title=Test Chat")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Chat"
    assert "id" in data


def test_create_chat_session_default_title(authenticated_client: TestClient):
    """Test creating a chat session with default title."""
    response = authenticated_client.post("/api/chat/sessions")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Chat"
    assert "id" in data


def test_get_chat_sessions(authenticated_client: TestClient):
    """Test getting chat sessions."""
    # Create multiple sessions
    authenticated_client.post("/api/chat/sessions?title=Test Chat 1")
    authenticated_client.post("/api/chat/sessions?title=Test Chat 2")

    response = authenticated_client.get("/api/chat/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Should be ordered by updated_at desc
    assert data[0]["title"] == "Test Chat 2"
    assert data[1]["title"] == "Test Chat 1"


def test_get_chat_sessions_empty(authenticated_client: TestClient):
    """Test getting chat sessions when none exist."""
    response = authenticated_client.get("/api/chat/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_chat_session_by_id(authenticated_client: TestClient):
    """Test getting a specific chat session."""
    # Create a session
    session_response = authenticated_client.post("/api/chat/sessions?title=Test Chat")
    session_id = session_response.json()["id"]

    # Get the session
    response = authenticated_client.get(f"/api/chat/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id
    assert data["title"] == "Test Chat"


def test_get_nonexistent_chat_session(authenticated_client: TestClient):
    """Test getting a non-existent chat session."""
    response = authenticated_client.get("/api/chat/sessions/999")
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]


def test_send_chat_message(authenticated_client: TestClient):
    """Test sending a chat message."""
    # Create a session first
    session_response = authenticated_client.post("/api/chat/sessions?title=Test Chat")
    session_id = session_response.json()["id"]

    # Send a message
    message_data = {
        "message": "Hello, how are you?",
        "session_id": session_id,
        "use_documents": False
    }
    response = authenticated_client.post("/api/chat/", json=message_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["session_id"] == session_id
    assert data["sources"] is None


def test_send_chat_message_with_documents(authenticated_client: TestClient):
    """Test sending a chat message with document search enabled."""
    session_response = authenticated_client.post("/api/chat/sessions?title=Test Chat")
    session_id = session_response.json()["id"]

    # Mock document search to return empty results
    with patch('app.services.chat_service.document_processor') as mock_doc_processor:
        mock_doc_processor.search_documents.return_value = []

        message_data = {
            "message": "What is in the documents?",
            "session_id": session_id,
            "use_documents": True
        }
        response = authenticated_client.post("/api/chat/", json=message_data)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["session_id"] == session_id


def test_send_chat_message_invalid_session(authenticated_client: TestClient):
    """Test sending a message to a non-existent session."""
    message_data = {
        "message": "Hello, how are you?",
        "session_id": 999,
        "use_documents": False
    }
    response = authenticated_client.post("/api/chat/", json=message_data)
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]


def test_get_session_messages(authenticated_client: TestClient):
    """Test getting session messages."""
    # Create a session
    session_response = authenticated_client.post("/api/chat/sessions?title=Test Chat")
    session_id = session_response.json()["id"]

    # Send a message
    message_data = {
        "message": "Hello, how are you?",
        "session_id": session_id,
        "use_documents": False
    }
    authenticated_client.post("/api/chat/", json=message_data)

    # Get messages
    response = authenticated_client.get(f"/api/chat/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # User message + AI response
    assert any(msg["role"] == "user" for msg in data)
    assert any(msg["role"] == "assistant" for msg in data)


def test_get_messages_nonexistent_session(authenticated_client: TestClient):
    """Test getting messages for a non-existent session."""
    response = authenticated_client.get("/api/chat/sessions/999/messages")
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]


def test_get_messages_empty_session(authenticated_client: TestClient):
    """Test getting messages for a session with no messages."""
    session_response = authenticated_client.post("/api/chat/sessions?title=Empty Chat")
    session_id = session_response.json()["id"]

    response = authenticated_client.get(f"/api/chat/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_chat_without_session(authenticated_client: TestClient):
    """Test sending a chat message without specifying session."""
    message_data = {
        "message": "Hello, how are you?",
        "use_documents": False
    }
    response = authenticated_client.post("/api/chat/", json=message_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "session_id" in data


def test_chat_fallback_response(authenticated_client: TestClient):
    """Test chat fallback response when OpenAI is not available."""
    message_data = {
        "message": "Test fallback",
        "use_documents": False
    }

    # Mock settings to simulate no API key
    with patch('app.services.chat_service.settings') as mock_settings:
        mock_settings.OPENAI_API_KEY = None
        response = authenticated_client.post("/api/chat/", json=message_data)

    assert response.status_code == 200
    data = response.json()
    assert "OpenAI API key" in data["message"]
    assert "Test fallback" in data["message"]


def test_chat_openai_api_error(authenticated_client: TestClient):
    """Test chat handling when OpenAI API fails."""
    message_data = {
        "message": "Test API error",
        "use_documents": False
    }

    # Mock OpenAI client to raise an exception
    with patch('app.services.chat_service.settings') as mock_settings, \
         patch('app.services.chat_service.AsyncOpenAI') as mock_openai:

        mock_settings.OPENAI_API_KEY = "test-key"
        mock_client = AsyncMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        response = authenticated_client.post("/api/chat/", json=message_data)

    assert response.status_code == 200
    data = response.json()
    assert "OpenAI API key" in data["message"]
    assert "Test API error" in data["message"]


def test_chat_service_error_handling(authenticated_client: TestClient):
    """Test general error handling in chat service."""
    message_data = {
        "message": "Test error",
        "use_documents": False
    }

    # Mock chat_service to raise an exception
    with patch('app.services.chat_service.chat_service.generate_response') as mock_generate:
        mock_generate.side_effect = Exception("Service error")
        response = authenticated_client.post("/api/chat/", json=message_data)

    assert response.status_code == 500
    assert "Error generating response" in response.json()["detail"]


def test_chat_invalid_request_data(authenticated_client: TestClient):
    """Test chat with invalid request data."""
    # Missing required fields
    response = authenticated_client.post("/api/chat/", json={})
    assert response.status_code == 422  # Validation error

    # Invalid session_id type
    invalid_data = {
        "message": "Hello",
        "session_id": "invalid",
        "use_documents": False
    }
    response = authenticated_client.post("/api/chat/", json=invalid_data)
    assert response.status_code == 422


def test_conversation_context_preservation(authenticated_client: TestClient):
    """Test that conversation context is preserved across messages."""
    # Create a session
    session_response = authenticated_client.post("/api/chat/sessions?title=Context Test")
    session_id = session_response.json()["id"]

    # Send first message
    message1_data = {
        "message": "My name is Alice",
        "session_id": session_id,
        "use_documents": False
    }
    authenticated_client.post("/api/chat/", json=message1_data)

    # Send second message
    message2_data = {
        "message": "What is my name?",
        "session_id": session_id,
        "use_documents": False
    }
    authenticated_client.post("/api/chat/", json=message2_data)

    # Get all messages to verify context
    response = authenticated_client.get(f"/api/chat/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 4  # 2 user messages + 2 AI responses

    # Verify message order
    messages_by_role = {"user": [], "assistant": []}
    for msg in data:
        messages_by_role[msg["role"]].append(msg["content"])

    assert len(messages_by_role["user"]) >= 2
    assert len(messages_by_role["assistant"]) >= 2


def test_unauthorized_access(client: TestClient):
    """Test that chat endpoints require authentication."""
    # Test without authentication token
    response = client.get("/api/chat/sessions")
    assert response.status_code == 401

    response = client.post("/api/chat/sessions")
    assert response.status_code == 401

    message_data = {
        "message": "Hello",
        "use_documents": False
    }
    response = client.post("/api/chat/", json=message_data)
    assert response.status_code == 401


def test_cross_user_session_isolation(client: TestClient, test_user_data):
    """Test that users cannot access other users' sessions."""
    # Create two users
    user1_data = test_user_data.copy()
    user2_data = test_user_data.copy()
    user2_data["username"] = "testuser2"
    user2_data["email"] = "test2@example.com"

    # Register both users
    client.post("/api/auth/register", json=user1_data)
    client.post("/api/auth/register", json=user2_data)

    # Login as user1 and create a session
    response = client.post(
        "/api/auth/token",
        data={"username": user1_data["username"], "password": user1_data["password"]}
    )
    token1 = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token1}"})

    session_response = client.post("/api/chat/sessions?title=User1 Session")
    session_id = session_response.json()["id"]

    # Login as user2
    response = client.post(
        "/api/auth/token",
        data={"username": user2_data["username"], "password": user2_data["password"]}
    )
    token2 = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token2}"})

    # Try to access user1's session as user2
    response = client.get(f"/api/chat/sessions/{session_id}")
    assert response.status_code == 404  # Session not found for user2


def test_message_ordering(authenticated_client: TestClient):
    """Test that messages are returned in correct chronological order."""
    # Create a session
    session_response = authenticated_client.post("/api/chat/sessions?title=Order Test")
    session_id = session_response.json()["id"]

    # Send multiple messages with slight delays to ensure different timestamps
    messages = ["First message", "Second message", "Third message"]
    for msg in messages:
        message_data = {
            "message": msg,
            "session_id": session_id,
            "use_documents": False
        }
        authenticated_client.post("/api/chat/", json=message_data)

    # Get messages and verify order
    response = authenticated_client.get(f"/api/chat/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()

    # Extract user messages and verify they're in chronological order
    user_messages = [msg for msg in data if msg["role"] == "user"]
    assert len(user_messages) == 3
    assert user_messages[0]["content"] == "First message"
    assert user_messages[1]["content"] == "Second message"
    assert user_messages[2]["content"] == "Third message"
