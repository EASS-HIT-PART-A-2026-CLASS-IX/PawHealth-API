"""Core domain logic and CRUD operation tests."""

import pytest
from app.models import Dog, WeightEntry, WeightAnalysis

# ============= BASIC HEALTH & CRUD TESTS =============

def test_health_check(client):
    """Test basic health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_dog_registration(client):
    """Test dog registration (CREATE)."""
    dog_data = {"name": "Joey", "breed": "Poodle", "age": 3, "is_favorite": True}
    response = client.post("/dogs", json=dog_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Joey"
    assert response.json()["breed"] == "Poodle"

def test_list_dogs(client):
    """Test listing dogs (READ)."""
    # Create a dog
    dog_data = {"name": "Rex", "breed": "German Shepherd", "age": 5}
    client.post("/dogs", json=dog_data)
    
    # List dogs
    response = client.get("/dogs")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Rex"

def test_update_dog(client):
    """Test dog update (PATCH)."""
    # Create a dog
    dog_data = {"name": "Buddy", "breed": "Golden", "age": 2}
    create_response = client.post("/dogs", json=dog_data)
    dog_id = create_response.json()["id"]
    
    # Update the dog
    update_data = {"is_favorite": True, "age": 3}
    response = client.patch(f"/dogs/{dog_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["is_favorite"] is True
    assert response.json()["age"] == 3

def test_delete_dog(client):
    """Test dog deletion (DELETE)."""
    # Create a dog
    dog_data = {"name": "Rover", "breed": "Labrador", "age": 4}
    create_response = client.post("/dogs", json=dog_data)
    dog_id = create_response.json()["id"]
    
    # Delete the dog
    response = client.delete(f"/dogs/{dog_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True
    
    # Verify it's gone
    response = client.get(f"/dogs/{dog_id}")
    assert response.status_code == 404

# ============= WEIGHT MANAGEMENT TESTS =============

def test_weight_validation(client):
    """Test that negative weights are rejected."""
    # Create a dog first
    dog_data = {"name": "Max", "breed": "Boxer"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Try to log negative weight
    response = client.post(
        "/health/weight",
        json={"dog_id": dog_id, "weight_kg": -5.5}
    )
    assert response.status_code == 422

def test_weight_logging(client):
    """Test logging a weight entry."""
    # Create a dog
    dog_data = {"name": "Luna", "breed": "Husky"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log weight
    response = client.post(
        "/health/weight",
        json={"dog_id": dog_id, "weight_kg": 28.5}
    )
    assert response.status_code == 201
    assert response.json()["weight_kg"] == 28.5

def test_get_weight_history(client):
    """Test retrieving weight history."""
    # Create a dog
    dog_data = {"name": "Daisy", "breed": "Beagle"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log multiple weights
    for weight in [15.0, 15.5, 16.0]:
        client.post("/health/weight", json={"dog_id": dog_id, "weight_kg": weight})
    
    # Get history
    response = client.get(f"/health/weight/{dog_id}")
    assert response.status_code == 200
    assert len(response.json()) == 3

# ============= DOMAIN LOGIC: WEIGHT ANALYSIS TESTS =============

def test_weight_analysis_healthy(client):
    """Test weight analysis when dog is at ideal weight."""
    # Create a dog with ideal weight
    dog_data = {"name": "Charlie", "breed": "Beagle", "ideal_weight_kg": 15.0}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log weight at ideal
    client.post("/health/weight", json={"dog_id": dog_id, "weight_kg": 15.0})
    
    # Get analysis
    response = client.get(f"/health/analysis/{dog_id}")
    assert response.status_code == 200
    analysis = response.json()
    assert analysis["status"] == "healthy"
    assert "ideal weight" in analysis["recommendation"].lower()

def test_weight_analysis_11kg_to_10kg(client):
    """Test the specific EX3 case: 11kg dog with 10kg ideal target.
    
    This is the core domain logic requirement:
    - Dog "Max" weighs 11kg
    - Ideal weight is 10kg
    - Variance is +1kg (10% overweight)
    - System should recommend caloric reduction
    """
    # Create dog with 10kg ideal target
    dog_data = {"name": "Max", "breed": "Cocker Spaniel", "ideal_weight_kg": 10.0}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log current weight of 11kg
    client.post("/health/weight", json={"dog_id": dog_id, "weight_kg": 11.0})
    
    # Get analysis
    response = client.get(f"/health/analysis/{dog_id}")
    assert response.status_code == 200
    analysis = response.json()
    
    # Verify analysis
    assert analysis["status"] == "overweight"
    assert analysis["variance_kg"] == 1.0
    assert analysis["variance_percent"] == 10.0
    assert "overweight" in analysis["recommendation"].lower()
    assert "calorie" in analysis["recommendation"].lower() or "reduce" in analysis["recommendation"].lower()

def test_weight_analysis_underweight(client):
    """Test weight analysis when dog is underweight."""
    # Create a dog with ideal weight
    dog_data = {"name": "Scout", "breed": "Poodle", "ideal_weight_kg": 20.0}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log weight below ideal
    client.post("/health/weight", json={"dog_id": dog_id, "weight_kg": 18.0})
    
    # Get analysis
    response = client.get(f"/health/analysis/{dog_id}")
    assert response.status_code == 200
    analysis = response.json()
    assert analysis["status"] == "underweight"
    assert analysis["variance_kg"] == -2.0
    assert "underweight" in analysis["recommendation"].lower()

def test_weight_analysis_no_ideal_weight(client):
    """Test weight analysis when ideal weight not set."""
    # Create dog without ideal weight
    dog_data = {"name": "Bailey", "breed": "Dachshund"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log weight
    client.post("/health/weight", json={"dog_id": dog_id, "weight_kg": 5.5})
    
    # Get analysis
    response = client.get(f"/health/analysis/{dog_id}")
    assert response.status_code == 200
    analysis = response.json()
    assert analysis["status"] == "unknown"
    assert "set an ideal weight" in analysis["recommendation"].lower()

# ============= FEEDING LOG TESTS =============

def test_feeding_log(client):
    """Test logging a feeding session."""
    # Create a dog
    dog_data = {"name": "Stella", "breed": "Pug"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log feeding
    response = client.post(
        "/health/feeding",
        json={"dog_id": dog_id, "food_name": "Chicken Rice", "calories": 500}
    )
    assert response.status_code == 201
    assert response.json()["food_name"] == "Chicken Rice"

def test_get_feeding_history(client):
    """Test retrieving feeding history."""
    # Create a dog
    dog_data = {"name": "Toby", "breed": "Corgi"}
    dog_response = client.post("/dogs", json=dog_data)
    dog_id = dog_response.json()["id"]
    
    # Log multiple feedings
    for food in ["Kibble", "Chicken", "Carrot"]:
        client.post(
            "/health/feeding",
            json={"dog_id": dog_id, "food_name": food}
        )
    
    # Get history
    response = client.get(f"/health/feeding/{dog_id}")
    assert response.status_code == 200
    assert len(response.json()) == 3
