from sqlmodel import SQLModel, create_engine, Session
import os

# Database file location
sqlite_url = "sqlite:///paw_health.db"

# Create the engine with multi-thread support for SQLite
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Initialize database and create all defined tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for providing a database session to routes."""
    with Session(engine) as session:
        yield session
