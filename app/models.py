from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date

class Dog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, index=True)
    breed: str = Field(min_length=2, index=True)
    date_of_birth: Optional[date] = None
    profile_picture: Optional[str] = None
    is_favorite: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    chip_number: Optional[str] = None
    emergency_vet_name: Optional[str] = None
    emergency_vet_phone: Optional[str] = None

class WeightEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    weight_kg: float = Field(gt=0)
    date: datetime = Field(default_factory=datetime.now)
    dog_id: int = Field(foreign_key="dog.id") # Linking to a specific dog

class FeedingLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount_grams: int = Field(gt=0)
    food_type: str = Field(min_length=2)
    timestamp: datetime = Field(default_factory=datetime.now)
    dog_id: int = Field(foreign_key="dog.id")

class MedicalRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment_name: str = Field(min_length=2)
    category: str
    summary: Optional[str] = None
    diagnosis: Optional[str] = None
    administered_date: datetime = Field(default_factory=datetime.now)
    next_due_date: Optional[datetime] = None
    is_completed: bool = Field(default=True)
    dog_id: int = Field(foreign_key="dog.id")
