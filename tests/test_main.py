from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_system_health():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_dog_registration():
    """Test creating a new dog profile."""
    dog_data = {"name": "Joey", "breed": "Poodle", "is_favorite": True}
    response = client.post("/dog", json=dog_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Joey"

def test_invalid_weight_validation():
    """Test that negative weights are rejected (Status 422)."""
    response = client.post("/weight", json={"weight_kg": -5.5})
    assert response.status_code == 422
