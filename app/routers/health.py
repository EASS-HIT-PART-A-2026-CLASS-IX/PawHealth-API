from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import WeightEntry, WeightEntryCreate, WeightEntryRead, FeedingLog, FeedingLogCreate, FeedingLogRead

router = APIRouter(prefix="/health", tags=["Health Logs"])

@router.post("/weight", response_model=WeightEntryRead, status_code=201)
def log_weight(entry: WeightEntryCreate, session: Session = Depends(get_session)):
    if entry.weight_kg <= 0: raise HTTPException(status_code=422, detail="Weight must be strictly positive")
    db_entry = WeightEntry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry

@router.post("/feeding", response_model=FeedingLogRead, status_code=201)
def log_feeding(log: FeedingLogCreate, session: Session = Depends(get_session)):
    db_log = FeedingLog.model_validate(log)
    session.add(db_log)
    session.commit()
    session.refresh(db_log)
    return db_log
