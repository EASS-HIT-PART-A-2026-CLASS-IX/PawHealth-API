import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, Query
from sqlmodel import Session, select, or_
from typing import List, Optional
from app.database import create_db_and_tables, get_session
from app.models import Dog, WeightEntry, MedicalRecord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PawHealth")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Pro", version="3.1.0", lifespan=lifespan)

@app.middleware("http")
async def log_performance(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info(f"Path: {request.url.path} | Duration: {duration:.2f}ms")
    return response

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "version": "3.1.0"}

@app.get("/dog", tags=["Profile"], response_model=List[Dog])
async def list_dogs(
    session: Session = Depends(get_session),
    search: Optional[str] = Query(None),
    favorites: bool = Query(False)
):
    statement = select(Dog)
    if search:
        statement = statement.where(or_(Dog.name.contains(search), Dog.breed.contains(search)))
    if favorites:
        statement = statement.where(Dog.is_favorite == True)
    return session.exec(statement).all()

@app.post("/dog", tags=["Profile"], response_model=Dog)
async def register_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog)
    session.commit()
    session.refresh(dog)
    return dog

@app.post("/weight", tags=["Health"], response_model=WeightEntry)
async def log_weight(entry: WeightEntry, session: Session = Depends(get_session)):
    if entry.weight_kg <= 0:
        raise HTTPException(status_code=422, detail="Weight must be positive")
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry
