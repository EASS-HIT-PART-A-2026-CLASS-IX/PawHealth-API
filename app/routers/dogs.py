from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Dog, DogRead, DogCreate, DogUpdate, WeightEntry, WeightEntryRead
from app.security import get_current_user, require_scope

router = APIRouter(tags=["Dogs"])

# In-memory idempotency store (process-scoped)
processed_keys: set = set()

# ============= DOG CRUD OPERATIONS =============

@router.get("/", response_model=List[DogRead])
def list_dogs(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    """List all dogs with pagination."""
    return session.exec(select(Dog).offset(offset).limit(limit)).all()

@router.post("/", response_model=DogRead, status_code=201)
def create_dog(dog: DogCreate, session: Session = Depends(get_session)):
    """Create a new dog profile."""
    db_dog = Dog.model_validate(dog)
    session.add(db_dog)
    session.commit()
    session.refresh(db_dog)
    return db_dog

@router.get("/{dog_id}", response_model=DogRead)
def get_dog(dog_id: int, session: Session = Depends(get_session)):
    """Get a specific dog profile."""
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog

@router.patch("/{dog_id}", response_model=DogRead)
def update_dog(dog_id: int, dog_update: DogUpdate, session: Session = Depends(get_session)):
    """Partially update a dog profile (PATCH)."""
    db_dog = session.get(Dog, dog_id)
    if not db_dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    update_data = dog_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dog, key, value)

    session.add(db_dog)
    session.commit()
    session.refresh(db_dog)
    return db_dog

@router.delete("/{dog_id}")
def delete_dog(dog_id: int, session: Session = Depends(get_session)):
    """Delete a dog profile."""
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    session.delete(dog)
    session.commit()
    return {"ok": True}

# ============= WEIGHT TRACKING =============

@router.get("/{dog_id}/weight", response_model=List[WeightEntryRead])
def get_dog_weights(dog_id: int, session: Session = Depends(get_session)):
    """Get weight history for a dog."""
    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    return session.exec(
        select(WeightEntry)
        .where(WeightEntry.dog_id == dog_id)
        .order_by(WeightEntry.date.desc())
    ).all()

# ============= PROTECTED OPERATIONS (REQUIRE AUTH) =============

@router.post("/{dog_id}/refresh")
async def refresh_dog(
    dog_id: int,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user),
    x_idempotency_key: str = Header(None)
):
    """Refresh dog data. Requires a valid JWT with scope=pet_owner."""
    require_scope(user, "pet_owner")

    dog = session.get(Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    # Idempotency check
    if x_idempotency_key:
        if x_idempotency_key in processed_keys:
            return {"status": "already_processed", "dog_id": dog_id}
        processed_keys.add(x_idempotency_key)

    session.refresh(dog)

    return {
        "status": "success",
        "dog_id": dog_id,
        "updated_by": user.get("username", "authenticated_user"),
        "scope": user.get("scope"),
    }
