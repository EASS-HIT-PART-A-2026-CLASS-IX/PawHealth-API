from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.database import create_db_and_tables, get_session
from app.models import FeedingLog

app = FastAPI(
    title="PawHealth API",
    description="Backend for tracking dog health metrics, medications, and nutrition",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """Initialize the database on application startup."""
    create_db_and_tables()

@app.get("/health", tags=["System"])
def health_check():
    """Check if the API service is operational."""
    return {"status": "healthy", "service": "PawHealth"}

@app.post("/feeding", tags=["Nutrition"])
def log_feeding(log: FeedingLog, session: Session = Depends(get_session)):
    """Record a new feeding event for the dog."""
    session.add(log)
    session.commit()
    session.refresh(log)
    return log
