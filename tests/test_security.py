import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_protected_route_without_token():
    # EX3 Requirement: Test should fail when token is missing
    response = client.post("/dogs/1/refresh")
    # We expect 401 (Unauthorized) or 403 (Forbidden) depending on logic
    assert response.status_code in [401, 403]

def test_healthz_is_public():
    # Public routes should still work
    response = client.get("/healthz")
    assert response.status_code == 200
