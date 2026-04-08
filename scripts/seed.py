from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models import Dog, MedicalRecord, FeedingLog
from datetime import datetime, timedelta

def run_seed():
    create_db_and_tables()
    with Session(engine) as session:
        if session.query(Dog).first():
            return
        
        # 1. Seed Dog
        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        
        # 2. Seed Medical (Vaccine due today)
        vaccine = MedicalRecord(
            treatment_name="Rabies", 
            category="Vaccine", 
            next_due_date=datetime.now()
        )
        session.add(vaccine)
        
        # 3. Seed Snack
        snack = FeedingLog(amount_grams=15, food_type="Peanut Butter Treat")
        session.add(snack)
        
        session.commit()
        print("Successfully seeded all modules: Profile, Medical, and Nutrition! 🐾")

if __name__ == "__main__":
    run_seed()
