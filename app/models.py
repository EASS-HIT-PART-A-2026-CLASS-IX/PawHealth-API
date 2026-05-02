from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

class Dog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: str
    age: Optional[int] = 0
    is_favorite: bool = False

class WeightEntry(SQLModel):
    dog_id: int
    weight_kg: float

    @field_validator('weight_kg')
    @classmethod
    def weight_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Weight must be positive')
        return v
