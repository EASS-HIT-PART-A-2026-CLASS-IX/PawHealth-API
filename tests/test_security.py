"""Security and authentication tests."""

import pytest
from app.security import create_access_token

# ============= SECURITY TESTS =============

def test_protected_route_without_token(client):
    """Test that protected routes return 401 without authentication."""
    response = client.post("/dogs/1/refresh")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_protected_route_with_invalid_token(client):
    """Test that malformed tokens are rejected."""
    headers = {"Authorization": "NotBearer invalid-token"}
    response = client.post("/dogs/1/refresh", headers=headers)
    assert response.status_code == 401

def test_protected_route_with_valid_token(client):
    """Test that valid JWT tokens are accepted."""
    # Create a valid token
    token = create_access_token({"sub": "test_user", "scope": "pet_owner"})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/dogs/1/refresh", headers=headers)
    # Will get 404 because dog doesn't exist, but auth passes
    assert response.status_code == 404

def test_protected_route_with_valid_token_and_dog(client):
    """Test full workflow with authentication and idempotency."""
    # Create a dog
    dog_data = {"name": "Secured", "breed": "Shepherd"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Create a valid token
    token = create_access_token({"sub": "test_user", "scope": "pet_owner"})
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Idempotency-Key": "unique-operation-123"
    }
    
    # Call protected endpoint
    response = client.post(f"/dogs/{dog_id}/refresh", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["updated_by"] == "test_user"

def test_idempotency_enforcement(client):
    """Test idempotency key prevents duplicate operations."""
    # Create a dog
    dog_data = {"name": "Idempotent", "breed": "Poodle"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Create token
    token = create_access_token({"sub": "test_user"})
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Idempotency-Key": "same-key-456"
    }
    
    # First request
    response1 = client.post(f"/dogs/{dog_id}/refresh", headers=headers)
    assert response1.status_code == 200
    assert response1.json()["status"] == "success"
    
    # Second request with same key - should return already_processed
    response2 = client.post(f"/dogs/{dog_id}/refresh", headers=headers)
    assert response2.status_code == 200
    assert response2.json()["status"] == "already_processed"

def test_healthz_is_public(client):
    """Test that health endpoints are public (no auth required)."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_telemetry_headers(client):
    """Test that trace IDs are propagated."""
    response = client.get("/healthz")
    assert "x-trace-id" in response.headers
    assert "x-request-id" in response.headers
    assert len(response.headers["x-trace-id"]) > 0
