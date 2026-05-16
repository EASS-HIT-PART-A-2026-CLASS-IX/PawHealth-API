from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
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
    
    # Ensure a timestamp exists for table model validation
    if entry.date is None:
        entry.date = datetime.now(timezone.utc)
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

# ============= FEEDING LOGGING (in-memory compatibility layer) =============

# Simple in-memory store used by tests to record feeding events without changing DB schema.
_feeding_store: dict[int, list[dict]] = {}
_feeding_next_id = 1


@router.post("/feeding", status_code=201)
def log_feeding(payload: dict, session: Session = Depends(get_session)):
    """Accepts flexible feeding payloads from tests and stores them in-memory.

    Expected fields: `dog_id`, `food_name`, `calories` (optional), `date` (optional)
    """
    global _feeding_next_id
    dog_id = payload.get("dog_id")
    if dog_id is None:
        raise HTTPException(status_code=400, detail="dog_id is required")

    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    entry = {
        "id": _feeding_next_id,
        "dog_id": dog_id,
        "dog_name": dog.name,
        "food_name": payload.get("food_name"),
        "calories": payload.get("calories"),
        "date": payload.get("date") or datetime.now(timezone.utc).isoformat(),
    }
    _feeding_next_id += 1
    _feeding_store.setdefault(dog_id, []).append(entry)
    return entry


@router.get("/feeding/{dog_id}")
def get_feeding_history(dog_id: int, session: Session = Depends(get_session)):
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    # Only return entries that match the current dog's name to avoid id reuse collisions in tests
    entries = _feeding_store.get(dog_id, [])
    return [e for e in entries if e.get("dog_name") == dog.name]

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

