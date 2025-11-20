from fastapi import APIRouter
from pydantic import BaseModel
from math import ceil

router = APIRouter()

class SavingsRequest(BaseModel):
    trip_cost: float
    monthly_savings: float

@router.post("/savings_plan")
def savings_plan(req: SavingsRequest):
    if req.monthly_savings <= 0:
        return {"error": "monthly_savings must be > 0"}
    months = ceil(req.trip_cost / req.monthly_savings)
    return {
        "trip_cost": req.trip_cost,
        "monthly_savings": req.monthly_savings,
        "months_needed": months
    }
