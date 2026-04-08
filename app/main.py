import time
import logging
from fastapi import FastAPI, Depends, Request
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from app.database import create_db_and_tables, get_session
from app.models import Dog, FeedingLog, WeightEntry, MedicalRecord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PawHealth")

app = FastAPI(
    title="PawHealth Pro",
    description="Advanced Veterinary Management API with proactive intelligence.",
    version="3.0.0"
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

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "PawHealth"}

@app.get("/tasks/today", tags=["Intelligence"])
def get_daily_tasks(session: Session = Depends(get_session)):
    tasks = []
    today = datetime.now().date()
    upcoming = session.exec(select(MedicalRecord).where(MedicalRecord.next_due_date <= today)).all()
    for item in upcoming:
        tasks.append({"task": f"Medical: {item.treatment_name}", "severity": "URGENT", "due_date": str(item.next_due_date.date())})
    return {"date": str(today), "pending_tasks": tasks, "total_count": len(tasks)}

@app.post("/dog", tags=["Profile"], response_model=Dog)
def register_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog)
    session.commit()
    session.refresh(dog)
    return dog

@app.get("/dog", tags=["Profile"], response_model=List[Dog])
def list_dogs(session: Session = Depends(get_session)):
    return session.exec(select(Dog)).all()

@app.post("/feeding", tags=["Nutrition"], response_model=FeedingLog)
def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    session.add(log)
    session.commit()
    session.refresh(log)
    return log

@app.post("/weight", tags=["Health"], response_model=WeightEntry)
def log_weight(entry: WeightEntry, session: Session = Depends(get_session)):
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry
