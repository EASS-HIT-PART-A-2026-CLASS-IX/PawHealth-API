import uuid
from fastapi import FastAPI, Depends, Response, Header, HTTPException
from .security import get_current_user

app = FastAPI(title="PawHealth API", version="EX3-Final")

# Simple in-memory store for idempotency (Session 09 requirement)
processed_keys = set()

@app.middleware("http")
async def add_telemetry_headers(request, call_next):
    """
    Telemetry Middleware: Propagates trace IDs (Session 12).
    """
    trace_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["x-trace-id"] = trace_id
    return response

@app.get("/healthz")
async def healthz():
    return {"status": "healthy", "version": "EX3-Final"}

@app.post("/dogs/{dog_id}/refresh")
async def refresh_dog(
    dog_id: int, 
    user: dict = Depends(get_current_user),
    x_idempotency_key: str = Header(None)
):
    """
    Protected route with Idempotency logic (Session 09).
    """
    if x_idempotency_key:
        if x_idempotency_key in processed_keys:
            return {"status": "already_processed", "dog_id": dog_id, "key": x_idempotency_key}
        processed_keys.add(x_idempotency_key)

    # Business logic for Joey (The King)
    return {
        "status": "success", 
        "dog_id": dog_id, 
        "updated_by": user["username"]
    }

@app.post("/dogs/analyze-food")
async def analyze_food(dog_breed: str, food: str):
    return {
        "is_safe": True, 
        "advice": f"For a {dog_breed}, {food} is safe. Always consult a vet."
    }
