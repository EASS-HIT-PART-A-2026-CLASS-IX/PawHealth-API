import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

# 1. Import models FIRST
from app.models import Pet

# 2. THEN import the FastAPI instance and database session
from app.main import app
from app.database import get_session

# Use StaticPool to keep the in-memory database shared across connections
sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
