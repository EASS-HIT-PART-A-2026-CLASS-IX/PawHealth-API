from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Pet, PetCreate
from app.database import get_session

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.post("/", response_model=Pet, status_code=201)
def create_pet(pet: PetCreate, session: Session = Depends(get_session)):
    db_pet = Pet.model_validate(pet)
    session.add(db_pet)
    session.commit()
    session.refresh(db_pet)
    return db_pet

@router.get("/", response_model=List[Pet])
def read_pets(session: Session = Depends(get_session)):
    pets = session.exec(select(Pet)).all()
    return pets
