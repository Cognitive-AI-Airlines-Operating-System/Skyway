from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthRequest(BaseModel):
    city: str
    country: str
    month: int

@router.post("/health")
def health(req: HealthRequest):
    alerts = []
    severity = "low"

    if req.month in (6, 7, 8):
        alerts.append("Monsoon season – carry rain gear and beware of floods.")
        severity = "medium"

    if req.city.lower() in ("delhi", "hyderabad"):
        alerts.append("Air quality can be poor – consider a mask on bad AQI days.")
        if severity == "low":
            severity = "medium"

    return {
        "city": req.city,
        "country": req.country,
        "severity": severity,
        "alerts": alerts
    }
