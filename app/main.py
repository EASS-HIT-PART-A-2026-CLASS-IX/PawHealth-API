import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .database import engine, create_db_and_tables
# Import ALL models so SQLModel registers them in metadata for table creation
from .models import (
    User, UserCreate, UserRead,
    Dog, DogRead, DogCreate, DogUpdate,
    WeightEntry, WeightEntryCreate, WeightEntryRead,
    FeedingLog, FeedingLogCreate, FeedingLogRead,
    WeightAnalysis
)
from .routers import dogs, health, system, auth

processed_keys = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    create_db_and_tables()
    yield

app = FastAPI(
    title="PawHealth API",
    version="EX3-Final",
    description="Smart veterinary management system for dog health",
    lifespan=lifespan
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MIDDLEWARE =============

@app.middleware("http")
async def add_telemetry_headers(request, call_next):
    """Add trace ID to all responses for telemetry tracking."""
    trace_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["x-trace-id"] = trace_id
    response.headers["x-request-id"] = trace_id
    return response

# ============= INCLUDE ROUTERS =============

app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(dogs, prefix="/dogs", tags=["Dogs"])
app.include_router(health, prefix="/health", tags=["Health"])
app.include_router(system, tags=["System"])

# ============= HEALTH CHECK ENDPOINTS =============

@app.get("/health")
@app.get("/healthz")
async def health_check():
    """System health check endpoint."""
    return {"status": "healthy", "version": "EX3-Final"}

# ============= WEIGHT ANALYSIS ENDPOINT =============

@app.get("/analysis/{dog_id}")
async def get_weight_analysis(dog_id: int):
    """Get weight analysis and recommendations for a dog.
    
    This endpoint demonstrates the domain logic for weight management:
    - Calculates variance from ideal weight
    - Provides personalized recommendations
    - Special handling for edge cases (e.g., 11kg dog with 10kg target)
    """
    with Session(engine) as session:
        dog = session.get(Dog, dog_id)
        if not dog:
            return {"error": "Dog not found", "dog_id": dog_id}
        
        # Get latest weight
        latest_weight = session.exec(
            select(WeightEntry)
            .where(WeightEntry.dog_id == dog_id)
            .order_by(WeightEntry.date.desc())
        ).first()
        
        if not latest_weight:
            return {"error": "No weight data found", "dog_id": dog_id}
        
        # Generate analysis
        analysis = WeightAnalysis.from_dog_and_weight(dog, latest_weight.weight_kg)
        return analysis.model_dump()

# ============= AI FOOD ANALYSIS ENDPOINT =============

@app.post("/dogs/analyze-food")
async def analyze_food(dog_breed: str, food: str):
    """Analyze if a food is safe for a dog breed.
    
    In production, this would call the sidecar AI service.
    """
    return {"is_safe": True, "advice": f"For a {dog_breed}, {food} is safe."}

