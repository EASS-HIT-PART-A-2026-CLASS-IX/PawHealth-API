from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uuid
from app.config import settings
# EX3 Requirement: Role-based access logic will be added here

app = FastAPI(title="PawHealth PRO API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response

@app.get("/healthz")
async def health():
    return {"status": "healthy", "version": "EX3-Final"}

@app.post("/dogs/analyze-food")
async def analyze_dog_food(dog_breed: str, food: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ai_sidecar_url}/analyze",
                json={"dog_breed": dog_breed, "food_item": food}
            )
            return response.json()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="AI Sidecar unavailable")

@app.post("/dogs/{dog_id}/refresh")
async def refresh_dog(dog_id: int, idempotency_key: str = Header(None)):
    return {"message": f"Dog {dog_id} refreshed", "idempotency_key": idempotency_key}
