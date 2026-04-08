from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Dog

def run_seed():
    create_db_and_tables()
    with Session(engine) as session:
        if session.exec(select(Dog)).first():
            return
        
        # Seed Dog with full Emergency Info
        joey = Dog(
            name="Joey", 
            breed="Poodle", 
            is_favorite=True,
            chip_number="985-111-000",
            emergency_vet_name="Dr. Barkwell (24/7 Clinic)",
            emergency_vet_phone="+972-50-000-0000"
        )
        session.add(joey)
        session.commit()
        print("Successfully seeded with Emergency SOS info! 🚨🐾")

if __name__ == "__main__":
    run_seed()
