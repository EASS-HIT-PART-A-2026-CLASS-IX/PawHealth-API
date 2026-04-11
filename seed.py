from sqlmodel import Session, create_engine, select, SQLModel
from app.models import Dog, WeightEntry
from datetime import datetime
import os

engine = create_engine("sqlite:///pawhealth.db")

def seed_data():
    # 1. This is the crucial fix! Create tables if they don't exist
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # 2. Fixed the deprecation warning by using select() and exec()
        if session.exec(select(Dog)).first(): 
            print("Database is already seeded!")
            return

        # Create Joey
        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        session.commit()
        session.refresh(joey)

        # Log Joey's initial weight
        weight = WeightEntry(weight_kg=5.5, dog_id=joey.id)
        session.add(weight)
        session.commit()
        print(f"Successfully seeded Joey (ID: {joey.id}) and his initial weight!")

if __name__ == "__main__":
    seed_data()
