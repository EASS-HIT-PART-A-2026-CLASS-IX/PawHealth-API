from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import field_validator

# --- USER MODELS ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    username: str
    password: str

class UserRead(SQLModel):
    id: int
    username: str
    created_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# --- DOG MODELS ---
class Dog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: str
    age: Optional[int] = 0
    is_favorite: bool = False
    ideal_weight_kg: float
    current_weight_kg: float
    medical_history: Optional[str] = None
    photo_filename: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DogCreate(SQLModel):
    name: str
    breed: str
    age: Optional[int] = 0
    is_favorite: Optional[bool] = False
    ideal_weight_kg: float
    current_weight_kg: float
    medical_history: Optional[str] = None
    photo_filename: Optional[str] = None

class DogUpdate(SQLModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    is_favorite: Optional[bool] = None
    ideal_weight_kg: Optional[float] = None
    current_weight_kg: Optional[float] = None
    medical_history: Optional[str] = None
    photo_filename: Optional[str] = None

class DogRead(Dog):
    pass

# --- NEW: CLINIC VISITS ---
class ClinicVisit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    visit_date: datetime = Field(default_factory=datetime.utcnow)
    reason: str
    notes: Optional[str] = None
    next_checkup_date: Optional[datetime] = None

# --- NEW: VACCINATIONS ---
class Vaccination(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    vaccine_name: str
    date_administered: datetime = Field(default_factory=datetime.utcnow)
    next_due_date: Optional[datetime] = None

# --- WEIGHT & FEEDING ---
class WeightEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    weight_kg: float
    date: datetime = Field(default_factory=datetime.utcnow)

class WeightEntryCreate(SQLModel):
    dog_id: int
    weight_kg: float
    date: Optional[datetime] = None

class WeightEntryRead(WeightEntry):
    pass

class FeedingLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    portion_size_g: float
    date: datetime = Field(default_factory=datetime.utcnow)

class FeedingLogCreate(SQLModel):
    dog_id: int
    portion_size_g: float
    date: Optional[datetime] = None

class FeedingLogRead(FeedingLog):
    pass

class WeightAnalysis(SQLModel):
    dog_id: int
    name: str
    current_weight_kg: float
    ideal_weight_kg: float
    status: str
    recommendation: str

    @classmethod
    def from_dog_and_weight(cls, dog: Dog, current_weight: float) -> "WeightAnalysis":
        variance = current_weight - dog.ideal_weight_kg
        status = "healthy" if abs(variance) < 0.5 else ("overweight" if variance > 0 else "underweight")
        return cls(
            dog_id=dog.id, name=dog.name, current_weight_kg=current_weight,
            ideal_weight_kg=dog.ideal_weight_kg, status=status,
            recommendation=f"Personalized advice for {dog.name} based on {status} status."
        )