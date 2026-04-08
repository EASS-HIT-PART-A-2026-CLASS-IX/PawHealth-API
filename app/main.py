import time
import logging
import csv
import io
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select, or_
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import create_db_and_tables, get_session
from app.models import Dog, WeightEntry, MedicalRecord, FeedingLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PawHealth")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth Pro", version="3.4.0", lifespan=lifespan)

@app.get("/intelligence/health-score/{dog_id}", tags=["Intelligence"])
async def get_dog_health_score(dog_id: int, session: Session = Depends(get_session)):
    """Calculate a real-time health score based on medical and nutrition data."""
    # Logic: Start with 100, deduct points for overdue vaccines or lack of feeding
    score = 100
    recommendations = []
    
    # Check overdue vaccines
    overdue = session.exec(select(MedicalRecord).where(MedicalRecord.next_due_date < datetime.now())).all()
    if overdue:
        score -= len(overdue) * 15
        recommendations.append(f"Visit the vet for {overdue[0].treatment_name}")
        
    # Check feeding (did the dog eat in the last 24h?)
    last_day = datetime.now() - timedelta(days=1)
    feeding = session.exec(select(FeedingLog).where(FeedingLog.timestamp > last_day)).all()
    if not feeding:
        score -= 30
        recommendations.append("No feeding logged in the last 24 hours!")
        
    return {
        "score": max(score, 0),
        "status": "Excellent" if score > 80 else "Needs Attention",
        "recommendations": recommendations
    }

@app.get("/export/medical", tags=["System"])
async def export_medical_records(session: Session = Depends(get_session)):
    """Export all medical records to a professional CSV format."""
    records = session.exec(select(MedicalRecord)).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Treatment", "Category", "Summary", "Diagnosis", "Date", "Next Due"])
    
    for r in records:
        writer.writerow([r.id, r.treatment_name, r.category, r.summary, r.diagnosis, r.administered_date, r.next_due_date])
    
    output.seek(0)
    return StreamingResponse(
        output, 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment; filename=medical_history.csv"}
    )

# Standard CRUD continues below...
@app.post("/dog", tags=["Profile"], response_model=Dog)
async def register_dog(dog: Dog, session: Session = Depends(get_session)):
    session.add(dog); session.commit(); session.refresh(dog); return dog

@app.get("/dog", tags=["Profile"], response_model=List[Dog])
async def list_dogs(session: Session = Depends(get_session), search: Optional[str] = Query(None)):
    statement = select(Dog)
    if search:
        statement = statement.where(or_(Dog.name.contains(search), Dog.breed.contains(search)))
    return session.exec(statement).all()

@app.get("/emergency/sos", tags=["Emergency"])
async def get_sos_info(session: Session = Depends(get_session)):
    dogs = session.exec(select(Dog)).all()
    return [{"dog": d.name, "chip": d.chip_number, "vet": d.emergency_vet_phone} for d in dogs]

@app.post("/medical", tags=["Health"])
async def add_medical(record: MedicalRecord, session: Session = Depends(get_session)):
    session.add(record); session.commit(); session.refresh(record); return record

@app.post("/feeding", tags=["Nutrition"])
async def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    session.add(log); session.commit(); session.refresh(log); return log
