from sqlmodel import Session, create_engine
from app.models import Dog, WeightEntry
from datetime import datetime

engine = create_engine("sqlite:///pawhealth.db")

def seed_data():
    with Session(engine) as session:
        if session.query(Dog).first(): return

        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        session.commit()
        session.refresh(joey)

        weight = WeightEntry(weight_kg=5.5, dog_id=joey.id)
        session.add(weight)
        session.commit()
        print(f"Seeded Joey (ID: {joey.id}) with initial weight!")

if __name__ == "__main__":
    seed_data()
