from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="PawHealth Sidecar", version="EX3", description="AI-powered nutrition advisor for dogs")

# ============= MODELS =============

class FoodAnalysisRequest(BaseModel):
    dog_breed: str
    food_name: str

class FoodAnalysisResponse(BaseModel):
    is_safe: bool
    toxicity_risk: str  # "safe", "caution", "dangerous"
    explanation: str
    recommendations: Optional[str] = None

# ============= TOXICITY DATABASE =============
# In production, this would be an ML model or external API

TOXIC_FOODS = {
    "chocolate": {"risk": "dangerous", "reason": "Contains theobromine"},
    "xylitol": {"risk": "dangerous", "reason": "Causes hypoglycemia and liver damage"},
    "grapes": {"risk": "dangerous", "reason": "Kidney toxicity"},
    "raisins": {"risk": "dangerous", "reason": "Kidney toxicity"},
    "avocado": {"risk": "caution", "reason": "Persin toxin in high amounts"},
    "garlic": {"risk": "caution", "reason": "Thiosulfate oxidizes hemoglobin"},
    "onions": {"risk": "caution", "reason": "Thiosulfate toxicity"},
    "macadamia": {"risk": "caution", "reason": "Unknown toxic compound"},
    "apple": {"risk": "safe", "reason": "Safe in moderation; remove seeds"},
    "carrot": {"risk": "safe", "reason": "Low-calorie vegetable; excellent for teeth"},
    "pumpkin": {"risk": "safe", "reason": "Good source of fiber"},
    "chicken": {"risk": "safe", "reason": "High-quality protein"},
    "rice": {"risk": "safe", "reason": "Easy to digest"},
}

# ============= BREED-SPECIFIC RECOMMENDATIONS =============

BREED_CHARACTERISTICS = {
    "Golden Retriever": {"appetite": "high", "tendency": "overweight", "metabolism": "moderate"},
    "Chihuahua": {"appetite": "low", "tendency": "varies", "metabolism": "high"},
    "Labrador": {"appetite": "high", "tendency": "overweight", "metabolism": "moderate"},
    "Poodle": {"appetite": "moderate", "tendency": "varies", "metabolism": "high"},
    "German Shepherd": {"appetite": "high", "tendency": "lean", "metabolism": "high"},
}

# ============= ENDPOINTS =============

@app.get("/healthz")
def health_check():
    """Health check for Docker Compose."""
    return {"status": "ok", "service": "sidecar"}

@app.post("/analyze-food", response_model=FoodAnalysisResponse)
async def analyze_food(request: FoodAnalysisRequest) -> FoodAnalysisResponse:
    """Analyze if a food is safe for a specific dog breed.
    
    This endpoint demonstrates the AI sidecar improvement:
    - Checks food toxicity
    - Considers breed-specific metabolic factors
    - Provides evidence-based recommendations
    
    Examples:
    - Breed: "Golden Retriever", Food: "apple" → SAFE (with recommendations)
    - Breed: "Any", Food: "chocolate" → DANGEROUS (high risk)
    """
    food_lower = request.food_name.lower().strip()
    
    # Look up food in toxicity database
    if food_lower in TOXIC_FOODS:
        info = TOXIC_FOODS[food_lower]
        is_safe = info["risk"] == "safe"
        
        # Get breed info
        breed_info = BREED_CHARACTERISTICS.get(
            request.dog_breed,
            {"appetite": "moderate", "tendency": "varies", "metabolism": "moderate"}
        )
        
        recommendation = None
        if is_safe:
            if food_lower == "apple":
                recommendation = "Safe in moderation. Remove seeds. Good for dental health."
            elif food_lower == "carrot":
                recommendation = "Excellent low-calorie treat. Great for overweight dogs."
            elif food_lower in ["chicken", "rice"]:
                recommendation = "Good meal component. Suitable for sensitive stomachs."
        elif info["risk"] == "caution":
            recommendation = f"Use with caution for {request.dog_breed}. Consider breed metabolism: {breed_info['metabolism']}."
        
        return FoodAnalysisResponse(
            is_safe=is_safe,
            toxicity_risk=info["risk"],
            explanation=info["reason"],
            recommendations=recommendation
        )
    
    # Unknown food - safe assumption but caution
    return FoodAnalysisResponse(
        is_safe=True,
        toxicity_risk="safe",
        explanation="Food not in known toxicity database. Generally considered safe for dogs.",
        recommendations="Introduce new foods gradually. Monitor for allergic reactions. Consult vet if unsure."
    )

@app.get("/breed-info/{breed_name}")
async def get_breed_info(breed_name: str):
    """Get breed-specific metabolic information."""
    info = BREED_CHARACTERISTICS.get(
        breed_name,
        {"message": "Breed not in database", "fallback": "Use moderate portions"}
    )
    return {"breed": breed_name, "info": info}

