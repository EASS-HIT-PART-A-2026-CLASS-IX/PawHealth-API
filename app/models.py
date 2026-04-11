from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Dog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, index=True)
    breed: str = Field(min_length=2, index=True)
    is_favorite: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    weights: List["WeightEntry"] = Relationship(back_populates="dog")
    feedings: List["FeedingLog"] = Relationship(back_populates="dog")
    records: List["MedicalRecord"] = Relationship(back_populates="dog")

class WeightEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    weight_kg: float = Field(gt=0)
    date: datetime = Field(default_factory=datetime.now)
    dog_id: int = Field(foreign_key="dog.id")
    dog: Optional[Dog] = Relationship(back_populates="weights")

class FeedingLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount_grams: int = Field(gt=0)
    food_type: str = Field(min_length=2)
    timestamp: datetime = Field(default_factory=datetime.now)
    dog_id: int = Field(foreign_key="dog.id")
    dog: Optional[Dog] = Relationship(back_populates="feedings")

class MedicalRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment_name: str = Field(min_length=2)
    category: str
    administered_date: datetime = Field(default_factory=datetime.now)
    dog_id: int = Field(foreign_key="dog.id")
    dog: Optional[Dog] = Relationship(back_populates="records")
