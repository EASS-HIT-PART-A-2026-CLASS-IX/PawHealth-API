import time
import logging
from fastapi import FastAPI, Depends, Request
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from app.database import create_db_and_tables, get_session
from app.models import Dog, FeedingLog, WeightEntry, MedicalTreatment

# Professional Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PawHealth")

app = FastAPI(
    title="PawHealth API",
    description="Professional Dog Health Monitoring System",
    version="2.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Middleware for Request Timing and Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Method: {request.method} Path: {request.url.path} Time: {process_time:.2f}ms")
    return response

# --- Alerts & Insights ---
@app.get("/health/alerts", tags=["Insights"])
def get_health_alerts(session: Session = Depends(get_session)):
    """Analyze records and return urgent health alerts."""
    alerts = []
    now = datetime.now()
    
    # Check for overdue vaccines
    treatments = session.exec(select(MedicalTreatment)).all()
    for t in treatments:
        if t.next_due_date and t.next_due_date < now:
            alerts.append({"severity": "HIGH", "msg": f"Vaccine {t.name} is overdue!"})
            
    return {"alerts": alerts, "total_alerts": len(alerts)}

# --- Core API (Dog, Feeding, Weight, Medical) ---
@app.post("/dog", tags=["Profile"])
def create_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog)
    session.commit()
    session.refresh(dog)
    return dog

@app.get("/dog", tags=["Profile"])
def get_dogs(session: Session = Depends(get_session)):
    return session.exec(select(Dog)).all()

@app.post("/feeding", tags=["Nutrition"])
def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    session.add(log)
    session.commit()
    session.refresh(log)
    return log

@app.post("/weight", tags=["Health"])
def log_weight(entry: WeightEntry, session: Session = Depends(get_session)):
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

@app.post("/medical", tags=["Health"])
def log_treatment(treatment: MedicalTreatment, session: Session = Depends(get_session)):
    session.add(treatment)
    session.commit()
    session.refresh(treatment)
    return treatment
