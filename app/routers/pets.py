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

@router.get("/{pet_id}", response_model=Pet)
def read_pet(pet_id: int, session: Session = Depends(get_session)):
    pet = session.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.put("/{pet_id}", response_model=Pet)
def update_pet(pet_id: int, pet_update: PetCreate, session: Session = Depends(get_session)):
    pet = session.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    pet_data = pet_update.model_dump(exclude_unset=True)
    pet.sqlmodel_update(pet_data)
    session.add(pet)
    session.commit()
    session.refresh(pet)
    return pet

@router.delete("/{pet_id}")
def delete_pet(pet_id: int, session: Session = Depends(get_session)):
    pet = session.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    session.delete(pet)
    session.commit()
    return {"message": "Pet deleted successfully"}
