from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Dog, DogRead, DogCreate, WeightEntry, WeightEntryRead

router = APIRouter(prefix="/dogs", tags=["Dogs"])

@router.get("/", response_model=List[DogRead])
def list_dogs(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    return session.exec(select(Dog).offset(offset).limit(limit)).all()

@router.post("/", response_model=DogRead, status_code=201)
def create_dog(dog: DogCreate, session: Session = Depends(get_session)):
    db_dog = Dog.model_validate(dog)
    session.add(db_dog)
    session.commit()
    session.refresh(db_dog)
    return db_dog

@router.delete("/{dog_id}")
def delete_dog(dog_id: int, session: Session = Depends(get_session)):
    dog = session.get(Dog, dog_id)
    if not dog: raise HTTPException(status_code=404)
    session.delete(dog)
    session.commit()
    return {"ok": True}

@router.get("/{dog_id}/weight", response_model=List[WeightEntryRead])
def get_dog_weights(dog_id: int, session: Session = Depends(get_session)):
    return session.exec(select(WeightEntry).where(WeightEntry.dog_id == dog_id)).all()
