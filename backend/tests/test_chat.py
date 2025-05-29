"""
Chat tests.
"""

import pytest
from fastapi.testclient import TestClient


def test_create_chat_session(authenticated_client: TestClient):
    """Test creating a chat session."""
    response = authenticated_client.post("/api/chat/sessions?title=Test Chat")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Chat"
    assert "id" in data


def test_get_chat_sessions(authenticated_client: TestClient):
    """Test getting chat sessions."""
    # Create a session first
    authenticated_client.post("/api/chat/sessions?title=Test Chat")
    
    response = authenticated_client.get("/api/chat/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Chat"


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
