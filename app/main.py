import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import dogs

app = FastAPI(title="PawHealth API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id") or f"paw-{uuid.uuid4().hex[:8]}"
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(dogs.router)

@app.get("/healthz", tags=["health"])
def healthcheck():
    return {"status": "ok", "database": "active"}
