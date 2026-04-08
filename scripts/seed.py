from sqlmodel import Session
from app.database import engine
from app.models import Dog, MedicalRecord
from datetime import datetime, timedelta

def run_seed():
    """Seed the database with initial demonstration data."""
    with Session(engine) as session:
        # Check if data already exists
        if session.query(Dog).first():
            print("Database already contains data. Skipping seed.")
            return

        # Create demo dog
        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        
        # Create a medical event
        vaccine = MedicalRecord(
            treatment_name="Rabies Vaccine",
            category="Vaccine",
            next_due_date=datetime.now() + timedelta(days=365)
        )
        session.add(vaccine)
        
        session.commit()
        print("Successfully seeded PawHealth with demo data! 🐾")

if __name__ == "__main__":
    run_seed()
