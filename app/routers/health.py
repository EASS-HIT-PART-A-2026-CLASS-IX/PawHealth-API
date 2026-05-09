from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import (
    WeightEntry, WeightEntryCreate, WeightEntryRead,
    FeedingLog, FeedingLogCreate, FeedingLogRead,
    Dog, WeightAnalysis
)

router = APIRouter(tags=["Health Logs"])

# ============= WEIGHT LOGGING =============

@router.post("/weight", response_model=WeightEntryRead, status_code=201)
def log_weight(entry: WeightEntryCreate, session: Session = Depends(get_session)):
    """Log a weight measurement for a dog."""
    if entry.weight_kg <= 0:
        raise HTTPException(status_code=422, detail="Weight must be strictly positive")
    
    # Verify dog exists
    dog = session.get(Dog, entry.dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    db_entry = WeightEntry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry

@router.get("/weight/{dog_id}", response_model=list[WeightEntryRead])
def get_weight_history(dog_id: int, session: Session = Depends(get_session)):
    """Get weight history for a dog."""
    # Verify dog exists
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    weights = session.exec(
        select(WeightEntry).where(WeightEntry.dog_id == dog_id).order_by(WeightEntry.date.desc())
    ).all()
    return weights

# ============= FEEDING LOGGING =============

@router.post("/feeding", response_model=FeedingLogRead, status_code=201)
def log_feeding(log: FeedingLogCreate, session: Session = Depends(get_session)):
    """Log a feeding session for a dog."""
    # Verify dog exists
    dog = session.get(Dog, log.dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    db_log = FeedingLog.model_validate(log)
    session.add(db_log)
    session.commit()
    session.refresh(db_log)
    return db_log

@router.get("/feeding/{dog_id}", response_model=list[FeedingLogRead])
def get_feeding_history(dog_id: int, session: Session = Depends(get_session)):
    """Get feeding history for a dog."""
    # Verify dog exists
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    logs = session.exec(
        select(FeedingLog).where(FeedingLog.dog_id == dog_id).order_by(FeedingLog.date.desc())
    ).all()
    return logs

# ============= WEIGHT ANALYSIS (Domain Logic) =============

@router.get("/analysis/{dog_id}", response_model=WeightAnalysis)
def get_weight_analysis(dog_id: int, session: Session = Depends(get_session)):
    """Get weight analysis and health recommendations.
    
    This endpoint demonstrates the core domain logic:
    - Calculates weight variance from ideal
    - Provides personalized recommendations
    - Handles edge cases (e.g., 11kg dog with 10kg target)
    
    Example: Dog "Max" weighs 11kg with 10kg ideal target:
    - Variance: +1kg (10% overweight)
    - Recommendation: Reduce calories by ~100kcal, increase exercise
    """
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    # Get latest weight
    latest_weight = session.exec(
        select(WeightEntry)
        .where(WeightEntry.dog_id == dog_id)
        .order_by(WeightEntry.date.desc())
    ).first()
    
    if not latest_weight:
        raise HTTPException(status_code=404, detail="No weight measurements found")
    
    # Generate analysis using domain logic
    analysis = WeightAnalysis.from_dog_and_weight(dog, latest_weight.weight_kg)
    return analysis

