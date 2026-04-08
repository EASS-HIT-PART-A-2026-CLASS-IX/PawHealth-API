import time
import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, Query, File, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select, or_
from typing import List, Optional
from datetime import datetime, date
from app.database import create_db_and_tables, get_session
from app.models import Dog, WeightEntry, MedicalRecord, FeedingLog

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    os.makedirs("uploads", exist_ok=True) # Ensure upload dir exists
    yield

app = FastAPI(title="PawHealth Ultimate", version="3.5.0", lifespan=lifespan)

# Mount static files so we can view the dog photos in the browser
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/dog/{dog_id}/analytics", tags=["Intelligence"])
async def get_dog_analytics(dog_id: int, session: Session = Depends(get_session)):
    """Calculate life stage and health metrics."""
    dog = session.get(Dog, dog_id)
    if not dog: raise HTTPException(status_code=44, detail="Dog not found")
    
    # Calculate Age & Life Stage
    life_stage = "Unknown"
    if dog.date_of_birth:
        age_years = (date.today() - dog.date_of_birth).days // 365
        if age_years < 2: life_stage = "Puppy"
        elif age_years < 7: life_stage = "Adult"
        else: life_stage = "Senior"
    
    return {"name": dog.name, "age_estimate": age_years, "life_stage": life_stage}

@app.post("/dog/{dog_id}/upload-photo", tags=["Profile"])
async def upload_dog_photo(dog_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    """Upload and save a profile picture for a dog."""
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
    """A unified chronological feed of ALL activities (Feeding, Medical, Weight)."""
    feedings = session.exec(select(FeedingLog)).all()
    medical = session.exec(select(MedicalRecord)).all()
    weights = session.exec(select(WeightEntry)).all()
    
    timeline = []
    for f in feedings: timeline.append({"type": "Feeding", "time": f.timestamp, "detail": f.food_type})
    for m in medical: timeline.append({"type": "Medical", "time": m.administered_date, "detail": m.treatment_name})
    for w in weights: timeline.append({"type": "Weight", "time": w.date, "detail": f"{w.weight_kg}kg"})
    
    return sorted(timeline, key=lambda x: x['time'], reverse=True)

# Standard endpoints below...
@app.get("/health", tags=["System"])
def health(): return {"status": "online"}

@app.post("/dog", tags=["Profile"], response_model=Dog)
def add_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog); session.commit(); session.refresh(dog); return dog
