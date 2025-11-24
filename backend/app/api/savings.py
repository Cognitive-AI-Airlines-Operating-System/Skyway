# backend/app/api/savings.py
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class SavingsRequest(BaseModel):
    budget: float = Field(gt=0, description="Total trip budget in INR")
    duration_days: int = Field(gt=0, description="Number of travel days")


@router.post("/savings")
def calculate_savings(req: SavingsRequest):
    """
    Very simple savings / daily-budget planner.

    Frontend calls this as POST /ai/savings (because of prefix in main.py).
    """
    daily_budget = round(req.budget / req.duration_days, 2)

    msg = (
        f"For a trip of {req.duration_days} days with total budget ₹{req.budget:.0f}, "
        f"you can spend about ₹{daily_budget:.0f} per day."
    )

    return {
        "total_budget": req.budget,
        "duration_days": req.duration_days,
        "daily_budget": daily_budget,
        "message": msg,
    }
