from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class DogBase(SQLModel):
    name: str = Field(min_length=1, index=True)
    breed: str = Field(min_length=2, index=True)
    is_favorite: bool = Field(default=False)
    chip_number: Optional[str] = None
    emergency_vet_name: Optional[str] = None
    emergency_vet_phone: Optional[str] = None

class Dog(DogBase, table=True):
    """Main Dog profile table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

class WeightEntry(SQLModel, table=True):
    """Tracking dog weight over time with strict validation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    weight_kg: float = Field(gt=0) # Must be positive
    date: datetime = Field(default_factory=datetime.now)
    dog_id: Optional[int] = None # Preparation for EX3 relations

class MedicalRecord(SQLModel, table=True):
    """Medical history and vaccine tracking."""
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment_name: str = Field(min_length=2)
    category: str # e.g., Vaccine, Surgery, Checkup
    administered_date: datetime = Field(default_factory=datetime.now)
    next_due_date: Optional[datetime] = None
