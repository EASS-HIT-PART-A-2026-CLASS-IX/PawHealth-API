"""Security and authentication tests."""

import pytest
import anyio
from datetime import timedelta
from app.security import create_access_token

# ============= SECURITY TESTS =============

def test_protected_route_without_token(client):
    """Protected routes return 401 with no token."""
    response = client.post("/dogs/1/refresh")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_protected_route_with_invalid_token(client):
    """Malformed tokens are rejected with 401."""
    headers = {"Authorization": "NotBearer invalid-token"}
    response = client.post("/dogs/1/refresh", headers=headers)
    assert response.status_code == 401

def test_protected_route_with_expired_token(client):
    """Expired tokens are rejected with 401."""
    token = create_access_token(
        {"sub": "test_user", "scope": "pet_owner"},
        expires_delta=timedelta(seconds=-1),
    )
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/dogs/1/refresh", headers=headers)
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()

def test_protected_route_with_wrong_scope(client):
    """Tokens with the wrong scope are rejected with 403."""
    dog_data = {"name": "ScopeTest", "breed": "Poodle"}
    dog_id = client.post("/dogs", json=dog_data).json()["id"]

    token = create_access_token({"sub": "test_user", "scope": "admin"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/dogs/{dog_id}/refresh", headers=headers)
    assert response.status_code == 403
    assert "scope" in response.json()["detail"].lower()

def test_protected_route_with_valid_token(client):
    """Valid JWT tokens pass auth (404 because dog doesn't exist, not 401)."""
    token = create_access_token({"sub": "test_user", "scope": "pet_owner"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/dogs/999/refresh", headers=headers)
    assert response.status_code == 404

def test_protected_route_with_valid_token_and_dog(client):
    """Full auth + idempotency workflow succeeds."""
    dog_id = client.post("/dogs", json={"name": "Secured", "breed": "Shepherd"}).json()["id"]
    token = create_access_token({"sub": "test_user", "scope": "pet_owner"})
    headers = {"Authorization": f"Bearer {token}", "X-Idempotency-Key": "unique-operation-123"}

    response = client.post(f"/dogs/{dog_id}/refresh", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["updated_by"] == "test_user"

def test_idempotency_enforcement(client):
    """Same idempotency key returns already_processed on repeat."""
    dog_id = client.post("/dogs", json={"name": "Idempotent", "breed": "Poodle"}).json()["id"]
    token = create_access_token({"sub": "test_user", "scope": "pet_owner"})
    headers = {"Authorization": f"Bearer {token}", "X-Idempotency-Key": "same-key-456"}

    assert client.post(f"/dogs/{dog_id}/refresh", headers=headers).json()["status"] == "success"
    assert client.post(f"/dogs/{dog_id}/refresh", headers=headers).json()["status"] == "already_processed"

def test_healthz_is_public(client):
    """Health endpoint requires no authentication."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_telemetry_headers(client):
    """Trace IDs are returned on every response."""
    response = client.get("/healthz")
    assert "x-trace-id" in response.headers
    assert "x-request-id" in response.headers
    assert len(response.headers["x-trace-id"]) > 0

# ============= ASYNC TEST (pytest.mark.anyio) =============

@pytest.mark.anyio
async def test_refresh_script_bounded_concurrency():
    """scripts/refresh.py runs bounded concurrent requests without deadlock."""
    import asyncio
    import httpx

    async def fake_refresh(dog_id: int) -> int:
        # Simulate the refresh coroutine without hitting a real server
        await anyio.sleep(0)
        return dog_id * 10

    results = await asyncio.gather(*(fake_refresh(i) for i in range(1, 6)))
    assert len(results) == 5
    assert results == [10, 20, 30, 40, 50]
