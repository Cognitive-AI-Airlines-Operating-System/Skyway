# backend/app/api/price.py
from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

router = APIRouter()
ROOT = Path(__file__).resolve().parents[2]  # repo/backend/
MODEL_PATH = ROOT / "data" / "artifacts" / "price_model.joblib"
model = joblib.load(MODEL_PATH)

class PriceRequest(BaseModel):
    airline: str
    source: str
    destination: str
    departure_date: str  # "YYYY-MM-DD"
    stops: int
    duration_mins: int
    days_to_dep: int

@router.post("/predict_price")
def predict_price(req: PriceRequest):
    date = pd.to_datetime(req.departure_date)
    row = {
        "airline": req.airline,
        "source": req.source,
        "destination": req.destination,
        "stops": req.stops,
        "duration_mins": req.duration_mins,
        "days_to_dep": req.days_to_dep,
        "month": date.month,
        "dow": date.dayofweek
    }
    X = pd.DataFrame([row])
    price = float(model.predict(X)[0])
    return {"predicted_price": round(price, 2)}
