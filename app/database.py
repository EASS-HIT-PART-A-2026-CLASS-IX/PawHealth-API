from sqlmodel import create_engine, Session, SQLModel
from .config import settings

def _build_engine():
    if settings.db_mode == "memory":
        connect_args = {"check_same_thread": False}
        return create_engine("sqlite://", connect_args=connect_args)
    
    connect_args = {"check_same_thread": False}
    return create_engine(settings.database_url, connect_args=connect_args)

engine = _build_engine()

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
