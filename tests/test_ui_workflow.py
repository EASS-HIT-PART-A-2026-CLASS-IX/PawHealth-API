import pytest

def test_ui_to_backend_flow(client):
    """Test UI workflow: Create dog via frontend client pattern."""
    # Create a dog (mimicking frontend workflow)
    dog_data = {"name": "Joey_Test", "breed": "Golden", "age": 3}
    create_response = client.post("/dogs", json=dog_data)
    assert create_response.status_code == 201
    
    # Get all dogs (mimicking frontend fetch)
    list_response = client.get("/dogs")
    assert list_response.status_code == 200
    dogs = list_response.json()
    
    # Verify our dog is in the list
    assert any(d["name"] == "Joey_Test" for d in dogs)

def test_frontend_integration_patterns(client):
    """Test patterns that frontend would use."""
    # Pattern 1: Get dogs with pagination
    response = client.get("/dogs?offset=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 0  # Empty initially
    
    # Pattern 2: Create dogs
    dog_ids = []
    for i in range(3):
        resp = client.post("/dogs", json={"name": f"Dog{i}", "breed": "Mixed"})
        assert resp.status_code == 201
        dog_ids.append(resp.json()["id"])
    
    # Pattern 3: Toggle favorite (PATCH)
    response = client.patch(f"/dogs/{dog_ids[0]}", json={"is_favorite": True})
    assert response.status_code == 200
    assert response.json()["is_favorite"] is True
    
    # Pattern 4: Get weight history
    response = client.get(f"/dogs/{dog_ids[0]}/weight")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

