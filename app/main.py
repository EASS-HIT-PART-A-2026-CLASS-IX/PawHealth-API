import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, Query
from sqlmodel import Session, select, or_
from typing import List, Optional
from datetime import datetime
from app.database import create_db_and_tables, get_session
from app.models import Dog, WeightEntry, MedicalRecord, FeedingLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PawHealth")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Pro", version="3.3.0", lifespan=lifespan)

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "version": "3.3.0"}

@app.get("/emergency/sos", tags=["Emergency"])
async def get_emergency_info(session: Session = Depends(get_session)):
    """Instant access to chip numbers and emergency vet contacts."""
    statement = select(Dog)
    dogs = session.exec(statement).all()
    sos_data = []
    for dog in dogs:
        sos_data.append({
            "dog_name": dog.name,
            "chip": dog.chip_number,
            "vet_name": dog.emergency_vet_name,
            "vet_phone": dog.emergency_vet_phone
        })
    return {"emergency_contacts": sos_data}

@app.post("/dog", tags=["Profile"], response_model=Dog)
async def register_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog); session.commit(); session.refresh(dog); return dog

@app.get("/dog", tags=["Profile"], response_model=List[Dog])
async def list_dogs(session: Session = Depends(get_session), search: Optional[str] = Query(None)):
    statement = select(Dog)
    if search:
        statement = statement.where(or_(Dog.name.contains(search), Dog.breed.contains(search)))
    return session.exec(statement).all()

@app.post("/weight", tags=["Health"], response_model=WeightEntry)
async def log_weight(entry: WeightEntry, session: Session = Depends(get_session)):
    if entry.weight_kg <= 0:
        raise HTTPException(status_code=422, detail="Weight must be positive")
    session.add(entry); session.commit(); session.refresh(entry); return entry

@app.post("/medical", tags=["Health"], response_model=MedicalRecord)
async def add_medical(record: MedicalRecord, session: Session = Depends(get_session)):
    session.add(record); session.commit(); session.refresh(record); return record

@app.post("/feeding", tags=["Nutrition"], response_model=FeedingLog)
async def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    session.add(log); session.commit(); session.refresh(log); return log
