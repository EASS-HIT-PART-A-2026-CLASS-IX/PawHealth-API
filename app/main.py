import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, func
from typing import List
from datetime import datetime, date
from app.database import create_db_and_tables, get_session
from app.models import Dog, FeedingLog, WeightEntry, MedicalRecord

app = FastAPI(title="PawHealth Pro", version="3.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- Emergency & Profile ---
@app.get("/emergency", tags=["Emergency"])
def get_emergency_info(session: Session = Depends(get_session)):
    """Quick access to emergency vet contact details."""
    dog = session.exec(select(Dog)).first()
    if not dog or not dog.emergency_vet_name:
        return {"msg": "No emergency contact set"}
    return {
        "vet_name": dog.emergency_vet_name,
        "phone": dog.emergency_vet_phone,
        "action": "CALL NOW"
    }

# --- Smart Task Engine ---
@app.get("/tasks/today", tags=["Intelligence"])
def get_daily_tasks(session: Session = Depends(get_session)):
    """Automatically generates a checklist for today's pet care."""
    tasks = []
    today = datetime.now().date()

    # 1. Check Feeding (Did Joey eat enough today?)
    today_start = datetime.combine(today, datetime.min.time())
    feedings = session.exec(select(FeedingLog).where(FeedingLog.timestamp >= today_start)).all()
    total_eaten = sum(f.amount_grams for f in feedings)
    if total_eaten < 200: # Target 200g
        tasks.append({"task": "Feeding", "status": "PENDING", "msg": f"Joey only ate {total_eaten}g out of 200g"})

    # 2. Check Upcoming/Overdue Medical
    upcoming = session.exec(select(MedicalRecord).where(MedicalRecord.next_due_date <= today)).all()
    for item in upcoming:
        tasks.append({
            "task": f"Medical: {item.treatment_name}",
            "status": "URGENT",
            "msg": f"Scheduled for: {item.next_due_date.date()}"
        })

    return {"date": today, "tasks": tasks, "count": len(tasks)}

# --- Standard Endpoints (Dog, Feeding, Medical) ---
@app.post("/dog", tags=["Profile"])
def update_dog_profile(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog)
    session.commit()
    session.refresh(dog)
    return dog

@app.post("/medical", tags=["Medical"])
def add_medical_record(record: MedicalRecord, session: Session = Depends(get_session)):
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@app.post("/feeding", tags=["Nutrition"])
def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    session.add(log)
    session.commit()
    session.refresh(log)
    return log
