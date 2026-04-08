import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, File, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from typing import List, Optional
from app.database import create_db_and_tables, get_session
from app.models import Dog, WeightEntry, MedicalRecord, FeedingLog

# Security: Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("uploads", exist_ok=True)
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Ultimate", version="3.6.0", lifespan=lifespan)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/dog/{dog_id}/upload-photo", tags=["Profile"])
async def upload_dog_photo(dog_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    # 1. Validate File Extension
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")
    
    dog = session.get(Dog, dog_id)
    if not dog: raise HTTPException(status_code=404, detail="Dog not found")
    
    # 2. Save File
    file_path = f"uploads/dog_{dog_id}.{extension}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    dog.profile_picture = file_path
    session.add(dog); session.commit(); session.refresh(dog)
    return {"status": "success", "path": file_path}

@app.post("/weight", tags=["Health"])
async def log_weight(entry: WeightEntry, session: Session = Depends(get_session)):
    # Ensure dog exists before linking weight
    if not session.get(Dog, entry.dog_id):
        raise HTTPException(status_code=404, detail="Dog not found")
    session.add(entry); session.commit(); session.refresh(entry); return entry

# ... [Keep other list/register endpoints as they were] ...
@app.get("/dog", tags=["Profile"], response_model=List[Dog])
async def list_dogs(session: Session = Depends(get_session)):
    return session.exec(select(Dog)).all()

@app.post("/dog", tags=["Profile"], response_model=Dog)
async def register_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog); session.commit(); session.refresh(dog); return dog

@app.get("/health", tags=["System"])
def health(): return {"status": "healthy"}
