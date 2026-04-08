from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Dog, WeightEntry, MedicalRecord

def run_seed():
    create_db_and_tables()
    with Session(engine) as session:
        if session.exec(select(Dog)).first():
            print("DB already seeded.")
            return
        
        # 1. Create Joey
        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        session.commit()
        session.refresh(joey) # Get Joey's generated ID
        
        # 2. Link data to Joey
        weight = WeightEntry(weight_kg=7.5, dog_id=joey.id)
        session.add(weight)
        
        vaccine = MedicalRecord(
            treatment_name="Rabies", 
            category="Vaccine", 
            dog_id=joey.id
        )
        session.add(vaccine)
        
        session.commit()
        print(f"Successfully seeded PawHealth for {joey.name} (ID: {joey.id})! 🐾")

if __name__ == "__main__":
    run_seed()
