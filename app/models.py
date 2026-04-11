from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class DogBase(SQLModel):
    name: str = Field(min_length=1, index=True)
    breed: str = Field(min_length=2, index=True)
    is_favorite: bool = Field(default=False)

class WeightEntryBase(SQLModel):
    weight_kg: float = Field(gt=0)
    dog_id: int = Field(foreign_key="dog.id")

class FeedingLogBase(SQLModel):
    amount_grams: int = Field(gt=0)
    food_type: str = Field(min_length=2)
    dog_id: int = Field(foreign_key="dog.id")

class Dog(DogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    weights: List["WeightEntry"] = Relationship(back_populates="dog")
    feedings: List["FeedingLog"] = Relationship(back_populates="dog")

class WeightEntry(WeightEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    dog: Optional[Dog] = Relationship(back_populates="weights")

class FeedingLog(FeedingLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    dog: Optional[Dog] = Relationship(back_populates="feedings")

class DogCreate(DogBase): pass
class DogRead(DogBase):
    id: int
    created_at: datetime

# NEW: Schema for partial updates
class DogUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1)
    breed: Optional[str] = Field(default=None, min_length=2)
    is_favorite: Optional[bool] = None

class WeightEntryCreate(WeightEntryBase): pass
class WeightEntryRead(WeightEntryBase):
    id: int
    date: datetime

class FeedingLogCreate(FeedingLogBase): pass
class FeedingLogRead(FeedingLogBase):
    id: int
    timestamp: datetime
