from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models import Dog

def run_seed():
    # Ensure tables exist before seeding
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if data already exists using the correct session.get or exec
        if session.query(Dog).first():
            print("Database already contains data. Skipping seed.")
            return

        joey = Dog(name="Joey", breed="Poodle", is_favorite=True)
        session.add(joey)
        session.commit()
        print("Successfully seeded PawHealth with demo data! 🐾")

if __name__ == "__main__":
    run_seed()
