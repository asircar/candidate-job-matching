from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import joblib
import os
from ..models.hybrid_matcher import HybridMatcher

app = FastAPI()

# Load the trained model
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'hybrid_model.joblib')
try:
    matcher = HybridMatcher.load(model_path)
except FileNotFoundError:
    matcher = None

class MatchRequest(BaseModel):
    candidate: Dict[str, Any]
    job: Dict[str, Any]

class MatchResponse(BaseModel):
    score: float
    feature_importance: Dict[str, float]
    feature_contribution: Dict[str, float] = None

@app.post("/match", response_model=MatchResponse)
async def match_candidate_job(request: MatchRequest):
    if matcher is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please train the model first.")
    
    try:
        score, explanation = matcher.predict_score(request.candidate, request.job)
        return MatchResponse(
            score=score,
            feature_importance=explanation['feature_importance'],
            feature_contribution=explanation['feature_contribution']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": matcher is not None} 