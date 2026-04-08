from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Dog, MedicalRecord
from datetime import datetime, timedelta

def run_seed():
    create_db_and_tables()
    with Session(engine) as session:
        if session.exec(select(Dog)).first():
            return
        
        # Seed Joey
        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        
        # Seed a detailed Medical Visit
        checkup = MedicalRecord(
            treatment_name="Annual Checkup",
            category="Routine",
            summary="Joey was a very good boy. Heart rate is normal, ears are clean.",
            diagnosis="Perfectly healthy poodle",
            next_due_date=datetime.now() + timedelta(days=365)
        )
        session.add(checkup)
        
        session.commit()
        print("Successfully seeded with detailed medical records! 🏥🐾")

if __name__ == "__main__":
    run_seed()
