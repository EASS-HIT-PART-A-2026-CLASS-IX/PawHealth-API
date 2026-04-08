from sqlmodel import Session, create_engine
from app.models import Dog, MedicalRecord
from datetime import datetime, timedelta

engine = create_engine("sqlite:///paw_health.db")

def seed_data():
    with Session(engine) as session:
        if session.query(Dog).first():
            print("Database already has data. Skipping seed.")
            return

        dogs = [
            Dog(name="Joey", breed="Poodle", is_favorite=True),
            Dog(name="Luna", breed="Golden Retriever"),
            Dog(name="Max", breed="German Shepherd")
        ]
        session.add_all(dogs)
        session.commit()
        print("Successfully seeded PawHealth with sample dogs! 🐾")

if __name__ == "__main__":
    seed_data()
