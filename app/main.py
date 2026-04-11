from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
from app.database import create_db_and_tables, get_session
from app.models import Dog, WeightEntry, FeedingLog, MedicalRecord
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Pro", version="3.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DOGS ---
@app.get("/dogs", tags=["Dogs"], response_model=List[Dog])
def list_dogs(
    offset: int = 0, 
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session)
):
    return session.exec(select(Dog).offset(offset).limit(limit)).all()

@app.post("/dogs", tags=["Dogs"], response_model=Dog, status_code=201)
def create_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog); session.commit(); session.refresh(dog); return dog

@app.delete("/dogs/{dog_id}", tags=["Dogs"])
def delete_dog(dog_id: int, session: Session = Depends(get_session)):
    dog = session.get(Dog, dog_id)
    if not dog: raise HTTPException(status_code=404)
    session.delete(dog); session.commit(); return {"ok": True}

# --- HEALTH LOGS (Weight) ---
@app.post("/health/weight", tags=["Health"], response_model=WeightEntry, status_code=201)
def log_weight(entry: WeightEntry, session: Session = Depends(get_session)):
    # Bulletproof manual validation to ensure 422 on negative weights
    if entry.weight_kg <= 0:
        raise HTTPException(status_code=422, detail="Weight must be strictly positive")
        
    session.add(entry); session.commit(); session.refresh(entry); return entry

@app.get("/dogs/{dog_id}/weight", tags=["Health"], response_model=List[WeightEntry])
def get_dog_weights(dog_id: int, session: Session = Depends(get_session)):
    return session.exec(select(WeightEntry).where(WeightEntry.dog_id == dog_id)).all()

# --- FEEDING ---
@app.post("/health/feeding", tags=["Health"], response_model=FeedingLog, status_code=201)
def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    session.add(log); session.commit(); session.refresh(log); return log

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "version": "3.2.0"}
