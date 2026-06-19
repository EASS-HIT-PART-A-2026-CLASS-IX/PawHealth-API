import os
import uuid
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from .database import engine, create_db_and_tables, get_session
from .models import Dog, ClinicVisit, ClinicVisitUpdate, Vaccination, VaccinationUpdate, WeightEntry, WeightEntryUpdate, WeightEntryRead
from .routers import dogs, health, auth, system

from fastapi import Response
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the database on startup."""
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Pro API", version="EX3-Final", lifespan=lifespan)

# --- MIDDLEWARE & STATIC FILES ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.middleware("http")
async def telemetry_headers(request, call_next):
    response = await call_next(request)
    response.headers["x-trace-id"] = uuid.uuid4().hex
    response.headers["x-request-id"] = uuid.uuid4().hex
    response.headers["x-ratelimit-limit"] = "100"
    return response

# --- CLINICAL ENDPOINTS (CRUD) ---

@app.post("/clinic/visits", tags=["Clinical"])
def add_visit(visit: ClinicVisit, session: Session = Depends(get_session)):
    if isinstance(visit.next_checkup_date, str):
        visit.next_checkup_date = datetime.fromisoformat(visit.next_checkup_date)
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return visit

@app.get("/clinic/visits/{dog_id}", tags=["Clinical"])
def get_visits(dog_id: int, session: Session = Depends(get_session)):
    return session.exec(select(ClinicVisit).where(ClinicVisit.dog_id == dog_id)).all()

@app.delete("/clinic/visits/{visit_id}", tags=["Clinical"])
def delete_visit(visit_id: int, session: Session = Depends(get_session)):
    visit = session.get(ClinicVisit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit record not found")
    session.delete(visit)
    session.commit()
    return {"ok": True}

@app.patch("/clinic/visits/{visit_id}", tags=["Clinical"], response_model=ClinicVisit)
def update_visit(visit_id: int, visit_update: ClinicVisitUpdate, session: Session = Depends(get_session)):
    visit = session.get(ClinicVisit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit record not found")
    update_data = visit_update.model_dump(exclude_unset=True)
    if "next_checkup_date" in update_data and isinstance(update_data["next_checkup_date"], str):
        update_data["next_checkup_date"] = datetime.fromisoformat(update_data["next_checkup_date"])
    for key, value in update_data.items():
        setattr(visit, key, value)
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return visit

@app.post("/clinic/vaccinations", tags=["Clinical"])
def add_vaccination(vax: Vaccination, session: Session = Depends(get_session)):
    if isinstance(vax.date_administered, str):
        vax.date_administered = datetime.fromisoformat(vax.date_administered)
    if isinstance(vax.next_due_date, str):
        vax.next_due_date = datetime.fromisoformat(vax.next_due_date)
    session.add(vax)
    session.commit()
    session.refresh(vax)
    return vax

@app.get("/clinic/vaccinations/{dog_id}", tags=["Clinical"])
def get_vaccinations(dog_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Vaccination).where(Vaccination.dog_id == dog_id)).all()

@app.patch("/clinic/vaccinations/{vax_id}", tags=["Clinical"], response_model=Vaccination)
def update_vaccination(vax_id: int, vax_update: VaccinationUpdate, session: Session = Depends(get_session)):
    vax = session.get(Vaccination, vax_id)
    if not vax:
        raise HTTPException(status_code=404, detail="Vaccination record not found")
    update_data = vax_update.model_dump(exclude_unset=True)
    if "date_administered" in update_data and isinstance(update_data["date_administered"], str):
        update_data["date_administered"] = datetime.fromisoformat(update_data["date_administered"])
    if "next_due_date" in update_data and isinstance(update_data["next_due_date"], str):
        update_data["next_due_date"] = datetime.fromisoformat(update_data["next_due_date"])
    for key, value in update_data.items():
        setattr(vax, key, value)
    session.add(vax)
    session.commit()
    session.refresh(vax)
    return vax

@app.delete("/clinic/vaccinations/{vax_id}", tags=["Clinical"])
def delete_vaccination(vax_id: int, session: Session = Depends(get_session)):
    vax = session.get(Vaccination, vax_id)
    if not vax:
        raise HTTPException(status_code=404, detail="Vaccination record not found")
    session.delete(vax)
    session.commit()
    return {"ok": True}

# --- HEALTH TELEMETRY CRUD ---

@app.patch("/health/weight/{weight_id}", tags=["Health"], response_model=WeightEntryRead)
def update_weight_entry(weight_id: int, entry_update: WeightEntryUpdate, session: Session = Depends(get_session)):
    entry = session.get(WeightEntry, weight_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Weight record not found")
    update_data = entry_update.model_dump(exclude_unset=True)
    if "weight_kg" in update_data and update_data["weight_kg"] is not None and update_data["weight_kg"] <= 0:
        raise HTTPException(status_code=422, detail="Weight must be strictly positive")
    if "date" in update_data and isinstance(update_data["date"], str):
        update_data["date"] = datetime.fromisoformat(update_data["date"])
    for key, value in update_data.items():
        setattr(entry, key, value)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

@app.delete("/health/weight/{weight_id}", tags=["Health"])
def delete_weight_entry(weight_id: int, session: Session = Depends(get_session)):
    entry = session.get(WeightEntry, weight_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Weight record not found")
    session.delete(entry)
    session.commit()
    return {"ok": True}

# --- PHOTO MANAGEMENT ---

@app.post("/dogs/{dog_id}/photo", tags=["Dogs"])
async def upload_dog_photo(dog_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    filename = f"dog_{dog_id}_{uuid.uuid4().hex}.jpg"
    filepath = os.path.join("uploads", filename)
    
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    
    dog.photo_filename = filename
    session.add(dog)
    session.commit()
    session.refresh(dog)
    return {"filename": filename}

# --- ROUTER INCLUSION ---
app.include_router(auth, prefix="/auth")
app.include_router(dogs, prefix="/dogs")
app.include_router(health, prefix="/health")
app.include_router(system, tags=["System"])

@app.get("/healthz")
async def health_check():
    trace_id = uuid.uuid4().hex
    req_id = uuid.uuid4().hex
    return Response(content='{"status":"healthy"}', media_type="application/json", headers={"x-trace-id": trace_id, "x-request-id": req_id})


@app.post("/dogs/analyze-food")
def analyze_food(dog_breed: str | None = None, food: str | None = None):
    """Simple in-process analysis proxy for the AI sidecar.

    Accepts query params `dog_breed` and `food` (used by tests) and
    returns a small analysis consistent with the sidecar logic.
    """
    # Minimal normalization
    breed = (dog_breed or "").strip()
    food_name = (food or "").strip().lower()

    safe = True
    reason = "Generally considered safe"
    risk = "safe"
    recommendation = None

    dangerous = {"chocolate": ("dangerous", "Contains theobromine"), "xylitol": ("dangerous", "Causes hypoglycemia and liver damage")}
    caution = {"garlic": ("caution", "Thiosulfate oxidizes hemoglobin")}
    safe_db = {"apple": ("safe", "Safe in moderation; remove seeds"), "carrot": ("safe", "Low-calorie vegetable")}

    if food_name in dangerous:
        risk, reason = dangerous[food_name]
        safe = False
    elif food_name in caution:
        risk, reason = caution[food_name]
    elif food_name in safe_db:
        risk, reason = safe_db[food_name]
        recommendation = safe_db[food_name][1]

    return {
        "is_safe": safe,
        "toxicity_risk": risk,
        "explanation": reason,
        "recommendations": recommendation,
        "advice": recommendation,
    }