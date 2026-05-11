from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator

# ============= USER MODELS =============

class User(SQLModel, table=True):
    """User account for authentication."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    """Schema for user registration."""
    username: str
    password: str

class UserRead(SQLModel):
    """Schema for reading user info (response)."""
    id: int
    username: str
    created_at: datetime

# ============= DOG MODELS =============

class Dog(SQLModel, table=True):
    """Dog profile with health tracking."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: str
    age: Optional[int] = 0
    is_favorite: bool = False
    ideal_weight_kg: Optional[float] = None  # Target weight for the dog
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DogCreate(SQLModel):
    """Schema for creating a new dog."""
    name: str
    breed: str
    age: Optional[int] = 0
    is_favorite: Optional[bool] = False
    ideal_weight_kg: Optional[float] = None

class DogUpdate(SQLModel):
    """Schema for updating a dog (PATCH)."""
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    is_favorite: Optional[bool] = None
    ideal_weight_kg: Optional[float] = None

class DogRead(Dog):
    """Schema for reading a dog (response)."""
    pass

# ============= WEIGHT ENTRY MODELS =============

class WeightEntry(SQLModel, table=True):
    """Weight measurement log for a dog."""
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int
    weight_kg: float
    date: datetime = Field(default_factory=datetime.utcnow)

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

    @field_validator('weight_kg')
    @classmethod
    def weight_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Weight must be positive')
        return v

class WeightEntryRead(WeightEntry):
    """Schema for reading a weight entry (response)."""
    pass

# ============= FEEDING LOG MODELS =============

class FeedingLog(SQLModel, table=True):
    """Feeding session log."""
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_id: int
    food_name: str
    calories: Optional[float] = None
    date: datetime = Field(default_factory=datetime.utcnow)

class FeedingLogCreate(SQLModel):
    """Schema for creating a feeding log."""
    dog_id: int
    food_name: str
    calories: Optional[float] = None

class FeedingLogRead(FeedingLog):
    """Schema for reading a feeding log (response)."""
    pass

# ============= WEIGHT ANALYSIS & DOMAIN LOGIC =============

class WeightAnalysis(SQLModel):
    """Weight analysis and recommendation for a dog."""
    dog_id: int
    name: str
    current_weight_kg: float
    ideal_weight_kg: Optional[float]
    variance_kg: Optional[float]  # current - ideal
    variance_percent: Optional[float]  # (current - ideal) / ideal * 100
    status: str  # "healthy", "overweight", "underweight", "unknown"
    recommendation: str
    
    @classmethod
    def from_dog_and_weight(cls, dog: Dog, current_weight: float) -> "WeightAnalysis":
        """Generate analysis from dog profile and current weight."""
        if dog.ideal_weight_kg is None:
            return cls(
                dog_id=dog.id,
                name=dog.name,
                current_weight_kg=current_weight,
                ideal_weight_kg=None,
                variance_kg=None,
                variance_percent=None,
                status="unknown",
                recommendation="Set an ideal weight target to receive personalized recommendations."
            )
        
        variance = current_weight - dog.ideal_weight_kg
        variance_pct = (variance / dog.ideal_weight_kg) * 100 if dog.ideal_weight_kg > 0 else 0
        
        # Determine status and generate recommendation
        if abs(variance) < 0.5:  # Within 0.5kg tolerance
            status = "healthy"
            recommendation = f"✓ {dog.name} is at ideal weight ({dog.ideal_weight_kg}kg). Maintain current diet and exercise routine."
        elif variance > 0:  # Overweight
            status = "overweight"
            excess = variance
            caloric_reduction = excess * 100  # Rough estimate: 100 cal per kg
            recommendation = f"⚠ {dog.name} is {excess:.1f}kg overweight. Reduce daily calories by ~{caloric_reduction:.0f} kcal. Increase exercise to 45+ min/day."
        else:  # Underweight
            status = "underweight"
            deficit = abs(variance)
            caloric_increase = deficit * 100
            recommendation = f"⚠ {dog.name} is {deficit:.1f}kg underweight. Increase daily calories by ~{caloric_increase:.0f} kcal. Consult vet if sudden weight loss."
        
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
