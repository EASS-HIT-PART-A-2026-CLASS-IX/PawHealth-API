from sqlmodel import create_engine, SQLModel, Session
from .config import settings

def _build_engine():
    if settings.db_mode == "memory":
        return create_engine("sqlite://")
    connect_args = {"check_same_thread": False} if settings.db_mode == "sqlite" else {}
    return create_engine(settings.database_url, echo=settings.database_echo, connect_args=connect_args)

engine = _build_engine()

def init_db():
    from . import models 
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
