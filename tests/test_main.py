from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Verify that the API is up and running."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "PawHealth"}

def test_create_dog():
    """Verify that a dog profile can be created successfully."""
    response = client.post("/dog", json={
        "name": "Joey",
        "breed": "Poodle",
        "chip_number": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Joey"
    assert "id" in data

def test_invalid_weight():
    """Verify that negative weight input returns a validation error (422)."""
    response = client.post("/weight", json={"weight_kg": -10})
    assert response.status_code == 422
