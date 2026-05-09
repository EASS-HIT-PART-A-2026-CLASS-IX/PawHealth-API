"""Shared pytest configuration and fixtures for all tests."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session

# ============= SHARED TEST DATABASE =============

@pytest.fixture(scope="function")
def test_engine():
    """Create a fresh in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def test_session(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session

@pytest.fixture(scope="function")
def client(test_engine):
    """Create a test client with overridden dependencies."""
    def get_session_override():
        with Session(test_engine) as session:
            yield session
    
    app.dependency_overrides[get_session] = get_session_override
    
    test_client = TestClient(app)
    yield test_client
    
    app.dependency_overrides.clear()
