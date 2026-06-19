import json
import os

import anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="PawHealth Sidecar", version="EX3", description="AI-powered nutrition advisor for dogs")

_client: Optional[anthropic.Anthropic] = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


class FoodAnalysisRequest(BaseModel):
    dog_breed: str
    food_name: str


class FoodAnalysisResponse(BaseModel):
    is_safe: bool
    toxicity_risk: str  # "safe", "caution", "dangerous"
    explanation: str
    recommendations: Optional[str] = None


@app.get("/healthz")
def health_check():
    return {"status": "ok", "service": "sidecar"}


@app.post("/analyze-food", response_model=FoodAnalysisResponse)
async def analyze_food(request: FoodAnalysisRequest) -> FoodAnalysisResponse:
    prompt = (
        f"You are a veterinary nutrition expert. Analyze whether '{request.food_name}' "
        f"is safe for a {request.dog_breed} dog to eat.\n\n"
        "Return a JSON object with exactly these fields:\n"
        '- is_safe (boolean): true if generally safe, false if dangerous or requires caution\n'
        '- toxicity_risk (string): one of "safe", "caution", or "dangerous"\n'
        "- explanation (string): brief explanation of why it is or isn't safe\n"
        "- recommendations (string or null): optional feeding advice or alternatives\n\n"
        "Return only valid JSON, no markdown code fences or extra text."
    )

    try:
        message = get_client().messages.create(
            model="claude-opus-4-8",
            max_tokens=512,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {e}")

    text = next(
        (block.text for block in message.content if block.type == "text"),
        None,
    )
    if not text:
        raise HTTPException(status_code=502, detail="Empty response from AI service")

    try:
        data = json.loads(text)
        return FoodAnalysisResponse(**data)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        raise HTTPException(status_code=502, detail=f"Failed to parse AI response: {e}")
