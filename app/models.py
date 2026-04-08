from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Dog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: str
    chip_number: Optional[str] = None

class WeightEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    weight_kg: float
    date: datetime = Field(default_factory=datetime.now)

class FeedingLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount_grams: int
    food_type: str
    timestamp: datetime = Field(default_factory=datetime.now)

class MedicalTreatment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str  # e.g., Vaccine, Pill, Surgery
    date: datetime
    next_due_date: Optional[datetime] = None
