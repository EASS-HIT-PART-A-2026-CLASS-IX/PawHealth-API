from fastapi.testclient import TestClient

def test_create_pet(client: TestClient):
    response = client.post(
        "/pets/",
        json={"name": "Buddy", "species": "Dog", "age": 3}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Buddy"
    assert data["id"] is not None

def test_read_pets(client: TestClient):
    # Insert a pet first
    client.post("/pets/", json={"name": "Luna", "species": "Cat", "age": 2})
    
    response = client.get("/pets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Luna"
