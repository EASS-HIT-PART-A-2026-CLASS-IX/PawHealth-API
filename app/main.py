import time
import os
import shutil
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, Query, File, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select, or_
from typing import List, Optional
from datetime import datetime, date
from app.database import create_db_and_tables, get_session
from app.models import Dog, WeightEntry, MedicalRecord, FeedingLog

# Ensure uploads directory exists BEFORE mounting
os.makedirs("uploads", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Ultimate", version="3.5.1", lifespan=lifespan)

# Mount static files for dog photos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "version": "3.5.1"}

@app.post("/dog/{dog_id}/upload-photo", tags=["Profile"])
async def upload_dog_photo(dog_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    dog = session.get(Dog, dog_id)
    if not dog: raise HTTPException(status_code=404, detail="Dog not found")
    
    file_path = f"uploads/dog_{dog_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    dog.profile_picture = file_path
    session.add(dog); session.commit(); session.refresh(dog)
    return {"info": "Photo uploaded successfully", "path": file_path}

@app.get("/timeline", tags=["Intelligence"])
async def get_unified_timeline(session: Session = Depends(get_session)):
    feedings = session.exec(select(FeedingLog)).all()
    medical = session.exec(select(MedicalRecord)).all()
    weights = session.exec(select(WeightEntry)).all()
    
    timeline = []
    for f in feedings: timeline.append({"type": "Feeding", "time": f.timestamp, "detail": f.food_type})
    for m in medical: timeline.append({"type": "Medical", "time": m.administered_date, "detail": m.treatment_name})
    for w in weights: timeline.append({"type": "Weight", "time": w.date, "detail": f"{w.weight_kg}kg"})
    
    return sorted(timeline, key=lambda x: x['time'], reverse=True)

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
