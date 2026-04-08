import time
import logging
from fastapi import FastAPI, Depends, Request
from sqlmodel import Session, select, func
from typing import List
from datetime import datetime, timedelta
from app.database import create_db_and_tables, get_session
from app.models import Dog, FeedingLog, WeightEntry, MedicalTreatment

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PawHealth")

app = FastAPI(
    title="PawHealth Pro API",
    description="Advanced Engineering Project for Dog Health & Nutrition Monitoring",
    version="2.5.0",
    contact={"name": "Bar Aizenberg", "url": "https://github.com/baraiz"}
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info(f"REQ: {request.method} {request.url.path} | DUR: {duration:.2f}ms | STATUS: {response.status_code}")
    return response

# --- Analytics & Insights ---
@app.get("/analytics/summary", tags=["Analytics"])
def get_health_summary(session: Session = Depends(get_session)):
    """Provides high-level health insights and statistics."""
    # Calculate Average Feeding
    avg_feeding = session.exec(select(func.avg(FeedingLog.amount_grams))).one()
    
    # Check for recent weight
    latest_weight = session.exec(select(WeightEntry).order_by(WeightEntry.date.desc())).first()
    
    # Overdue Vaccines
    overdue = session.exec(select(MedicalTreatment).where(MedicalTreatment.next_due_date < datetime.now())).all()
    
    return {
        "nutrition": {"average_daily_grams": round(avg_feeding, 2) if avg_feeding else 0},
        "latest_metrics": {"weight_kg": latest_weight.weight_kg if latest_weight else None},
        "alerts": {"overdue_treatments_count": len(overdue)}
    }

# --- Core API ---
@app.post("/dog", tags=["Profile"], response_model=Dog)
def create_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog)
    session.commit()
    session.refresh(dog)
    return dog

@app.get("/dog", tags=["Profile"], response_model=List[Dog])
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
