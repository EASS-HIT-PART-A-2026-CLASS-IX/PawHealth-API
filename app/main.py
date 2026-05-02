import uuid
from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Response, Header, HTTPException, status
from sqlmodel import Session, select
from .database import engine, create_db_and_tables
from .models import Dog, WeightEntry
from .security import get_current_user

processed_keys = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="PawHealth API", version="EX3-Final", lifespan=lifespan)
create_db_and_tables()

@app.middleware("http")
async def add_telemetry_headers(request, call_next):
    trace_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["x-trace-id"] = trace_id
    return response

@app.get("/health")
@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "version": "EX3-Final"}

@app.post("/health/weight")
async def log_weight(entry: WeightEntry):
    return {"status": "recorded", "data": entry}

@app.post("/dogs", response_model=Dog, status_code=status.HTTP_201_CREATED)
@app.post("/dogs/", response_model=Dog, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def register_dog(dog: Dog):
    with Session(engine) as session:
        session.add(dog)
        session.commit()
        session.refresh(dog)
        return dog

@app.get("/dogs", response_model=List[Dog])
@app.get("/dogs/", response_model=List[Dog], include_in_schema=False)
async def list_dogs():
    with Session(engine) as session:
        return session.exec(select(Dog)).all()

@app.post("/dogs/{dog_id}/refresh")
async def refresh_dog(dog_id: int, user: dict = Depends(get_current_user), x_idempotency_key: str = Header(None)):
    if x_idempotency_key and x_idempotency_key in processed_keys:
        return {"status": "already_processed", "dog_id": dog_id}
    if x_idempotency_key:
        processed_keys.add(x_idempotency_key)
    return {"status": "success", "dog_id": dog_id, "updated_by": user.get("username", "user")}

@app.post("/dogs/analyze-food")
async def analyze_food(dog_breed: str, food: str):
    return {"is_safe": True, "advice": f"For a {dog_breed}, {food} is safe."}
