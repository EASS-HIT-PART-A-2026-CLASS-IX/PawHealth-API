from sqlmodel import SQLModel, Field
from typing import Optional

# Base model for shared properties
class PetBase(SQLModel):
    name: str
    species: str
    age: int
    owner_email: Optional[str] = None

# Table model (Database)
class Pet(PetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Schema for creating a pet (API Input)
class PetCreate(PetBase):
    pass
