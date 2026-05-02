import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Security Tests (Session 11)
def test_unauthorized_access():
    """EX3: Verify that protected routes return 401 without a token."""
    response = client.post("/dogs/1/refresh")
    assert response.status_code == 401

def test_authorized_access():
    """EX3: Verify that protected routes work with a Bearer token."""
    headers = {"Authorization": "Bearer fake-token-for-ex3"}
    response = client.post("/dogs/1/refresh", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

# 2. Public Route & Telemetry Tests (Session 12)
def test_healthz_and_telemetry():
    """EX3: Verify health check and trace ID propagation."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert "x-trace-id" in response.headers

# 3. Idempotency Tests (Session 09)
def test_idempotency_enforcement():
    """EX3: Verify that repeating a request with the same key returns the idempotency status."""
    headers = {
        "Authorization": "Bearer fake-token-for-ex3",
        "X-Idempotency-Key": "unique-key-123"
    }
    # First request
    response1 = client.post("/dogs/1/refresh", headers=headers)
    assert response1.json()["status"] == "success"
    
    # Second request with same key
    response2 = client.post("/dogs/1/refresh", headers=headers)
    assert response2.json()["status"] == "already_processed"

# 4. AI Enhancement Test (The "Joey" feature)
def test_ai_food_analysis():
    """EX3: Verify the AI sidecar integration (mocked)."""
    response = client.post("/dogs/analyze-food?dog_breed=Golden&food=apple")
    assert response.status_code == 200
    assert "is_safe" in response.json()
