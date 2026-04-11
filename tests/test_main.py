import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session

# Setup in-memory database for testing (so we don't ruin the real DB)
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)

def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_dog_registration():
    # Calling the new plural endpoint '/dogs' and expecting 201 Created
    dog_data = {"name": "Joey", "breed": "Poodle", "is_favorite": True}
    response = client.post("/dogs", json=dog_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Joey"

def test_invalid_weight_validation():
    # 1. First, create a dog to get a valid dog_id
    dog_res = client.post("/dogs", json={"name": "Rex", "breed": "German Shepherd"})
    dog_id = dog_res.json()["id"]

    # 2. Try to log a negative weight using the new endpoint '/health/weight'
    response = client.post("/health/weight", json={"weight_kg": -5.5, "dog_id": dog_id})
    
    # 3. Pydantic should catch the negative number and return 422 Unprocessable Entity
    assert response.status_code == 422
