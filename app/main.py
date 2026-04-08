from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.models import Dog, Vaccination, WeightEntry, FeedingLog

app = FastAPI(title="PawHealth API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "PawHealth"}

@app.post("/feeding")
def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    session.add(log)
    session.commit()
    session.refresh(log)
    return log
