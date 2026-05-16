from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import field_validator

# ============= USER MODELS =============

class User(SQLModel, table=True):
    """User account for authentication."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(SQLModel):
    """Schema for user registration."""
    username: str
    password: str

class UserRead(SQLModel):
    """Schema for reading user info (response)."""
    id: int
    username: str
    created_at: datetime

class Token(SQLModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"

# ============= DOG MODELS =============

class Dog(SQLModel, table=True):
    """Dog profile with health tracking."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: str
    age: Optional[int] = 0
    is_favorite: bool = False
    ideal_weight_kg: Optional[float] = None
    current_weight_kg: Optional[float] = None
    medical_history: Optional[str] = None
    photo_filename: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DogCreate(SQLModel):
    """Schema for creating a new dog."""
    name: str
    breed: str
    age: Optional[int] = 0
    is_favorite: Optional[bool] = False
    ideal_weight_kg: Optional[float] = None
    current_weight_kg: Optional[float] = None
    medical_history: Optional[str] = None

class DogUpdate(SQLModel):
    """Schema for updating a dog (PATCH)."""
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    is_favorite: Optional[bool] = None
    ideal_weight_kg: Optional[float] = None
    current_weight_kg: Optional[float] = None
    medical_history: Optional[str] = None
    photo_filename: Optional[str] = None

class DogRead(Dog):
    """Schema for reading a dog (response)."""
    pass

# ============= CLINICAL MODELS =============

class ClinicVisit(SQLModel, table=True):
    """Clinical visit record."""
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    visit_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str
    notes: Optional[str] = None
    next_checkup_date: Optional[datetime] = None

class ClinicVisitUpdate(SQLModel):
    reason: Optional[str] = None
    notes: Optional[str] = None
    next_checkup_date: Optional[datetime] = None

class Vaccination(SQLModel, table=True):
    """Vaccination record."""
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    vaccine_name: str
    date_administered: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    next_due_date: Optional[datetime] = None

class VaccinationUpdate(SQLModel):
    vaccine_name: Optional[str] = None
    date_administered: Optional[datetime] = None
    next_due_date: Optional[datetime] = None

# ============= TELEMETRY MODELS =============

class WeightEntry(SQLModel, table=True):
    """Weight measurement log for a dog."""
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    weight_kg: float
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator('weight_kg')
    @classmethod
    def weight_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Weight must be positive')
        return v

class WeightEntryCreate(SQLModel):
    """Schema for creating a weight entry."""
    dog_id: int
    weight_kg: float
    date: Optional[datetime] = None

class WeightEntryUpdate(SQLModel):
    weight_kg: Optional[float] = None
    date: Optional[datetime] = None

class WeightEntryRead(WeightEntry):
    """Schema for reading a weight entry (response)."""
    pass

class FeedingLog(SQLModel, table=True):
    """Feeding session log."""
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int = Field(foreign_key="dog.id")
    portion_size_g: float
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FeedingLogCreate(SQLModel):
    """Schema for creating a feeding log."""
    dog_id: int
    portion_size_g: float
    date: Optional[datetime] = None

class FeedingLogRead(FeedingLog):
    """Schema for reading a feeding log (response)."""
    pass

# ============= DOMAIN LOGIC =============

class WeightAnalysis(SQLModel):
    """Weight analysis and recommendation for a dog."""
    dog_id: int
    name: str
    current_weight_kg: float
    ideal_weight_kg: float
    variance_kg: float
    variance_percent: float
    status: str  # "healthy", "overweight", "underweight"
    recommendation: str

    @classmethod
    def from_dog_and_weight(cls, dog: Dog, current_weight: float) -> "WeightAnalysis":
        """Generate clinical analysis from dog profile and current weight."""
        # If ideal weight is not set, return an "unknown" analysis prompting user to set ideal weight
        if not dog.ideal_weight_kg or dog.ideal_weight_kg <= 0:
            return cls(
                dog_id=dog.id,
                name=dog.name,
                current_weight_kg=current_weight,
                ideal_weight_kg=dog.ideal_weight_kg or 0.0,
                variance_kg=0.0,
                variance_percent=0.0,
                status="unknown",
                recommendation="Please set an ideal weight to enable analysis."
            )

        variance = current_weight - dog.ideal_weight_kg
        variance_pct = (variance / dog.ideal_weight_kg) * 100

        if abs(variance) < 0.5:
            status = "healthy"
            recommendation = f"✓ {dog.name} is at ideal weight. Maintain current lifestyle."
        elif variance > 0:
            status = "overweight"
            recommendation = f"⚠ {dog.name} is {variance:.1f}kg overweight. Reduce daily calories or portions to aid weight loss."
        else:
            status = "underweight"
            recommendation = f"⚠ {dog.name} is {abs(variance):.1f}kg underweight. Consult vet regarding feeding frequency."

        return cls(
            dog_id=dog.id,
            name=dog.name,
            current_weight_kg=current_weight,
            ideal_weight_kg=dog.ideal_weight_kg,
            variance_kg=round(variance, 2),
            variance_percent=round(variance_pct, 2),
            status=status,
            recommendation=recommendation
        )