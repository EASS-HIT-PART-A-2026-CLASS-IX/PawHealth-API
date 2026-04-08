import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import create_db_and_tables

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Create tables before running tests."""
    create_db_and_tables()

def test_system_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_dog_registration():
    dog_data = {"name": "Joey", "breed": "Poodle", "is_favorite": True}
    response = client.post("/dog", json=dog_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Joey"

def test_invalid_weight_validation():
    # We send dog_id: 1 (from seed/previous test) to pass the existence check
    # so we can actually test the negative weight validation logic
    response = client.post("/weight", json={"weight_kg": -5.5, "dog_id": 1})
    assert response.status_code == 422
