from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="PawHealth AI Sidecar")

class NutritionRequest(BaseModel):
    dog_breed: str
    food_item: str

@app.post("/analyze")
async def analyze_food(req: NutritionRequest):
    # This agent analyzes food safety for specific breeds
    toxic_items = ["chocolate", "grapes", "onions", "garlic"]
    is_safe = req.food_item.lower() not in toxic_items
    
    return {
        "is_safe": is_safe,
        "advice": f"For a {req.dog_breed}, {req.food_item} is {'safe' if is_safe else 'TOXIC'}. Always consult a vet."
    }

@app.get("/healthz")
def health():
    return {"status": "ok"}
