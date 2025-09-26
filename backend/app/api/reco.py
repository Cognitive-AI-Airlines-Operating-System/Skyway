# backend/app/api/reco.py
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import joblib
import numpy as np

router = APIRouter()
ROOT = Path(__file__).resolve().parents[3]  # repo/backend/
import os
from pathlib import Path
import pandas as pd

# Dynamically resolve the root directory (Skyway)
ROOT = Path(__file__).resolve().parents[2]

# Build paths relative to ROOT
PROC_PATH = ROOT / "data" / "processed" / "destinations_processed.csv"
ART = ROOT / "data" / "artifacts"

# Validate before loading
if not PROC_PATH.exists():
    raise FileNotFoundError(f"CSV file not found at: {PROC_PATH}")

# Load the data
DEST = pd.read_csv(PROC_PATH)

THEME_COLS = joblib.load(ART / "reco_theme_cols.joblib")

class RecoRequest(BaseModel):
    budget_total: float
    trip_days: int
    preferences: list[str] = []  # e.g., ["beach","culture"]

@router.post("/recommend_destinations")
def recommend_destinations(req: RecoRequest):
    df = DEST.copy()
    df["trip_cost"] = df["avg_daily_cost"] * req.trip_days
    affordable = df[df["trip_cost"] <= req.budget_total].copy()

    if affordable.empty:
        # If none affordable, return cheapest options
        df["trip_cost"] = df["avg_daily_cost"] * req.trip_days
        cheapest = df.nsmallest(10, "trip_cost")
        return cheapest[["city","country","region","trip_cost","avg_daily_cost","best_months"]].to_dict(orient="records")

    # Build preference score
    # Map incoming pref names to theme columns
    pref_map = {"beach":"theme_beach","culture":"theme_culture","adventure":"theme_adventure"}
    pref_score = np.zeros(len(affordable))
    for p in req.preferences:
        col = pref_map.get(p)
        if col and col in affordable.columns:
            pref_score += affordable[col].values

    # affordability score: lower cost -> higher score (normalized)
    max_cost = affordable["trip_cost"].max()
    if max_cost == 0: max_cost = 1
    affordability_score = 1 - (affordable["trip_cost"] / max_cost)

    # final score: weighted sum
    score = (pref_score * 1.2) + (affordability_score * 1.0)
    affordable["score"] = score
    top = affordable.sort_values("score", ascending=False).head(10)

    return top[["city","country","region","trip_cost","avg_daily_cost","best_months"]].to_dict(orient="records")



