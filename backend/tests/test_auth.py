"""
Authentication tests.
"""

import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient, test_user_data):
    """Test user registration."""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "id" in data


def test_register_duplicate_user(client: TestClient, test_user_data):
    """Test registering duplicate user."""
    # Register first user
    client.post("/api/auth/register", json=test_user_data)
    
    # Try to register same user again
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_user(client: TestClient, test_user_data):
    """Test user login."""
    # Register user
    client.post("/api/auth/register", json=test_user_data)
    
    # Login
    response = client.post(
        "/api/auth/token",
        data={"username": test_user_data["username"], "password": test_user_data["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, test_user_data):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/auth/token",
        data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_get_current_user(authenticated_client: TestClient, test_user_data):
    """Test getting current user information."""
    response = authenticated_client.get("/api/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]


def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without authentication."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401
