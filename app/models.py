from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Dog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1)
    breed: str
    chip_number: Optional[str] = None
    # Emergency Info
    emergency_vet_name: Optional[str] = None
    emergency_vet_phone: Optional[str] = None

class WeightEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    weight_kg: float = Field(gt=0)
    date: datetime = Field(default_factory=datetime.now)

class FeedingLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount_grams: int = Field(gt=0)
    food_type: str
    timestamp: datetime = Field(default_factory=datetime.now)

class MedicalRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment_name: str
    category: str  # Vaccine, Medication, Surgery, Checkup
    summary: Optional[str] = None  # Detailed visit summary
    diagnosis: Optional[str] = None
    administered_date: datetime = Field(default_factory=datetime.now)
    next_due_date: Optional[datetime] = None
    is_completed: bool = Field(default=True)
