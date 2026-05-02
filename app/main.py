import uuid
from fastapi import FastAPI, Depends, Response
from .security import get_current_user

app = FastAPI(title="PawHealth API", version="EX3-Final")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    """
    Telemetry Middleware: Adds a unique trace ID to every response header.
    """
    trace_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["x-trace-id"] = trace_id
    return response

@app.get("/healthz")
async def healthz():
    """
    Public health check endpoint.
    """
    return {"status": "healthy", "version": "EX3-Final"}

@app.post("/dogs/{dog_id}/refresh")
async def refresh_dog(dog_id: int, user: dict = Depends(get_current_user)):
    """
    Protected route: Requires a valid Bearer token.
    """
    return {
        "status": "success", 
        "dog_id": dog_id, 
        "updated_by": user["username"]
    }

@app.post("/dogs/analyze-food")
async def analyze_food(dog_breed: str, food: str):
    """
    Mock AI Analysis route for the demo script.
    """
    return {
        "is_safe": True, 
        "advice": f"For a {dog_breed}, {food} is safe. Always consult a vet."
    }
