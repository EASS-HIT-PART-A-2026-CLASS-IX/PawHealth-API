import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, Query
from sqlmodel import Session, select, or_
from typing import List, Optional
from app.database import create_db_and_tables, get_session
from app.models import Dog, FeedingLog, WeightEntry, MedicalRecord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PawHealth")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Pro", version="3.1.0", lifespan=lifespan)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "version": "3.1.0"}

@app.get("/dog", tags=["Profile"], response_model=List[Dog])
def list_dogs(
    session: Session = Depends(get_session),
    search: Optional[str] = Query(None, description="Search by name or breed"),
    favorites_only: bool = Query(False)
):
    statement = select(Dog)
    if search:
        statement = statement.where(or_(Dog.name.contains(search), Dog.breed.contains(search)))
    if favorites_only:
        statement = statement.where(Dog.is_favorite == True)
    return session.exec(statement).all()

@app.post("/dog", tags=["Profile"], response_model=Dog)
def register_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog); session.commit(); session.refresh(dog); return dog

@app.post("/weight", tags=["Health"])
def log_weight(entry: WeightEntry, session: Session = Depends(get_session)):
    session.add(entry); session.commit(); session.refresh(entry); return entry
