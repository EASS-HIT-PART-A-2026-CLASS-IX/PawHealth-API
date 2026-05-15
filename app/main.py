import uuid
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from .database import engine, create_db_and_tables, get_session
from .models import *
from .routers import dogs, health, system, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Pro API", version="EX3-Final", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded photos statically so the frontend can display them
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# New Clinical Endpoints
@app.post("/clinic/visits", tags=["Clinical"])
def add_visit(visit: ClinicVisit, session: Session = Depends(get_session)):
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return visit

@app.get("/clinic/visits/{dog_id}", tags=["Clinical"])
def get_visits(dog_id: int, session: Session = Depends(get_session)):
    return session.exec(select(ClinicVisit).where(ClinicVisit.dog_id == dog_id)).all()

@app.post("/clinic/vaccinations", tags=["Clinical"])
def add_vaccination(vax: Vaccination, session: Session = Depends(get_session)):
    session.add(vax)
    session.commit()
    session.refresh(vax)
    return vax

@app.get("/clinic/vaccinations/{dog_id}", tags=["Clinical"])
def get_vaccinations(dog_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Vaccination).where(Vaccination.dog_id == dog_id)).all()

# File upload endpoint
@app.post("/dogs/{dog_id}/photo", tags=["Dogs"])
async def upload_dog_photo(dog_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    """Upload a photo for a dog profile."""
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save file with unique name
    filename = f"dog_{dog_id}_{uuid.uuid4().hex}.jpg"
    filepath = os.path.join("uploads", filename)
    
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    
    # Update dog with photo filename
    dog.photo_filename = filename
    session.add(dog)
    session.commit()
    session.refresh(dog)
    
    return {"filename": filename, "dog_id": dog_id}

app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(dogs, prefix="/dogs", tags=["Dogs"])
app.include_router(health, prefix="/health", tags=["Health"])
app.include_router(system, tags=["System"])

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}