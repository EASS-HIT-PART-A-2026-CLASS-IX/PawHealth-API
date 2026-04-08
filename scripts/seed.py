from sqlmodel import Session
from app.database import engine
from app.models import Dog, MedicalRecord
from datetime import datetime, timedelta

def run_seed():
    with Session(engine) as session:
        if session.query(Dog).first():
            print("DB already contains data.")
            return
        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        session.commit()
        print("Successfully seeded! 🐾")

if __name__ == "__main__":
    run_seed()
