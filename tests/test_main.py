from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_dog():
    response = client.post("/dog", json={
        "name": "Joey",
        "breed": "Poodle",
        "chip_number": "123456"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Joey"

def test_invalid_weight():
    response = client.post("/weight", json={"weight_kg": -10})
    assert response.status_code == 422
