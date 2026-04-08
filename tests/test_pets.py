from fastapi.testclient import TestClient

def test_create_pet(client: TestClient):
    response = client.post("/pets/", json={"name": "Buddy", "species": "Dog", "age": 3})
    assert response.status_code == 201
    assert response.json()["name"] == "Buddy"

def test_read_pets(client: TestClient):
    client.post("/pets/", json={"name": "Luna", "species": "Cat", "age": 2})
    response = client.get("/pets/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_pet(client: TestClient):
    # 1. Create a pet
    create_resp = client.post("/pets/", json={"name": "Rocky", "species": "Dog", "age": 1})
    pet_id = create_resp.json()["id"]
    
    # 2. Update the pet's age
    update_resp = client.put(f"/pets/{pet_id}", json={"name": "Rocky", "species": "Dog", "age": 2})
    assert update_resp.status_code == 200
    assert update_resp.json()["age"] == 2

def test_delete_pet(client: TestClient):
    # 1. Create a pet
    create_resp = client.post("/pets/", json={"name": "Ghost", "species": "Parrot", "age": 10})
    pet_id = create_resp.json()["id"]
    
    # 2. Delete the pet
    del_resp = client.delete(f"/pets/{pet_id}")
    assert del_resp.status_code == 200
    
    # 3. Verify it's gone
    get_resp = client.get(f"/pets/{pet_id}")
    assert get_resp.status_code == 404
