from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Dog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, index=True)
    breed: str = Field(min_length=2, index=True)
    is_favorite: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    chip_number: Optional[str] = None
    emergency_vet_name: Optional[str] = None
    emergency_vet_phone: Optional[str] = None

class WeightEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    weight_kg: float = Field(gt=0)
    date: datetime = Field(default_factory=datetime.now)

class FeedingLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount_grams: int = Field(gt=0)
    food_type: str = Field(min_length=2)
    timestamp: datetime = Field(default_factory=datetime.now)

class MedicalRecord(SQLModel, table=True):
    """Detailed medical records including visit summaries and diagnoses."""
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment_name: str = Field(min_length=2)
    category: str # e.g., "Vaccine", "Checkup", "Emergency"
    
    # New fields for detailed clinical tracking
    summary: Optional[str] = None    # Notes about the visit
    diagnosis: Optional[str] = None  # Clinical diagnosis
    
    administered_date: datetime = Field(default_factory=datetime.now)
    next_due_date: Optional[datetime] = None
    is_completed: bool = Field(default=True)
