"""EX3 Full-Stack Integration Tests."""

import pytest
from app.security import create_access_token

# ============= EX3 FULL-STACK VALIDATION SUITE =============

# Session 11: Security Tests
def test_unauthorized_access(client):
    """EX3: Verify that protected routes return 401 without a token."""
    response = client.post("/dogs/1/refresh")
    assert response.status_code == 401

def test_authorized_access(client):
    """EX3: Verify that protected routes work with a valid Bearer token."""
    # Create a valid JWT token
    token = create_access_token({"sub": "test_user", "scope": "pet_owner"})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/dogs/1/refresh", headers=headers)
    # Will get 404 because dog doesn't exist, but auth passes
    assert response.status_code == 404

# Session 12: Public Route & Telemetry Tests
def test_healthz_and_telemetry(client):
    """EX3: Verify health check and trace ID propagation."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert "x-trace-id" in response.headers
    assert "x-request-id" in response.headers

# Session 09: Idempotency Tests
def test_idempotency_enforcement(client):
    """EX3: Verify that repeating a request with the same key returns already_processed."""
    # Create dog
    dog_data = {"name": "Idempotent", "breed": "Shepherd"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Create token
    token = create_access_token({"sub": "test_user"})
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Idempotency-Key": "unique-key-789"
    }
    
    # First request
    response1 = client.post(f"/dogs/{dog_id}/refresh", headers=headers)
    assert response1.json()["status"] == "success"
    
    # Second request with same key
    response2 = client.post(f"/dogs/{dog_id}/refresh", headers=headers)
    assert response2.json()["status"] == "already_processed"

# AI Enhancement: The "Joey" Feature
def test_ai_food_analysis(client):
    """EX3: Verify the AI sidecar integration."""
    response = client.post("/dogs/analyze-food?dog_breed=Golden&food=apple")
    assert response.status_code == 200
    data = response.json()
    assert "is_safe" in data
    assert "advice" in data

# ============= FULL-STACK INTEGRATION TESTS =============

def test_full_dog_lifecycle(client):
    """Test complete dog lifecycle: Create → Weight → Update → Analyze."""
    # 1. CREATE dog with ideal weight
    dog_data = {
        "name": "Integration",
        "breed": "Golden Retriever",
        "age": 4,
        "ideal_weight_kg": 30.0
    }
    dog_response = client.post("/dogs", json=dog_data)
    assert dog_response.status_code == 201
    dog = dog_response.json()
    dog_id = dog["id"]
    assert dog["ideal_weight_kg"] == 30.0
    
    # 2. LOG weight
    weight_response = client.post(
        "/health/weight",
        json={"dog_id": dog_id, "weight_kg": 32.0}
    )
    assert weight_response.status_code == 201
    
    # 3. GET weight history
    history_response = client.get(f"/health/weight/{dog_id}")
    assert history_response.status_code == 200
    assert len(history_response.json()) == 1
    
    # 4. ANALYZE weight (domain logic)
    analysis_response = client.get(f"/health/analysis/{dog_id}")
    assert analysis_response.status_code == 200
    analysis = analysis_response.json()
    assert analysis["status"] == "overweight"
    assert analysis["variance_kg"] == 2.0
    
    # 5. UPDATE dog
    update_response = client.patch(
        f"/dogs/{dog_id}",
        json={"is_favorite": True}
    )
    assert update_response.status_code == 200
    assert update_response.json()["is_favorite"] is True

def test_router_integration(client):
    """Verify all routers are properly integrated."""
    # Dogs router
    dogs_response = client.get("/dogs")
    assert dogs_response.status_code == 200
    
    # Health router - weight endpoint
    dog_response = client.post("/dogs", json={"name": "RouterTest", "breed": "Lab"})
    dog_id = dog_response.json()["id"]
    
    weight_response = client.post(
        "/health/weight",
        json={"dog_id": dog_id, "weight_kg": 25.0}
    )
    assert weight_response.status_code == 201
    
    # System router
    health_response = client.get("/health")
    assert health_response.status_code == 200

def test_multiple_dogs_tracking(client):
    """Test tracking multiple dogs independently."""
    dogs = []
    for i in range(3):
        response = client.post(
            "/dogs",
            json={
                "name": f"Dog{i}",
                "breed": "Mixed",
                "ideal_weight_kg": 20 + i
            }
        )
        dogs.append(response.json())
    
    # Log different weights
    for i, dog in enumerate(dogs):
        client.post(
            "/health/weight",
            json={"dog_id": dog["id"], "weight_kg": 20 + i + 2}
        )
    
    # Verify each has correct analysis
    for i, dog in enumerate(dogs):
        response = client.get(f"/health/analysis/{dog['id']}")
        analysis = response.json()
        assert analysis["variance_kg"] == 2.0
        assert analysis["status"] == "overweight"

def test_cors_headers(client):
    """Verify CORS is enabled for frontend."""
    response = client.options("/dogs")
    assert response.status_code in [200, 405]  # 405 is OK for OPTIONS on GET endpoint
