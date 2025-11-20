from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class DisruptionRequest(BaseModel):
    airline: str
    source: str
    destination: str
    departure_time: str

@router.post("/simulate")
def simulate(req: DisruptionRequest):
    status = random.choice(["on_time", "delayed", "cancelled"])
    delay_mins = 0
    reason = "N/A"

    if status == "delayed":
        delay_mins = random.choice([30, 45, 60, 90])
        reason = random.choice(["Weather", "Technical check", "Air traffic"])
    elif status == "cancelled":
        reason = random.choice(["Operational issues", "Severe weather"])

    return {
        "airline": req.airline,
        "source": req.source,
        "destination": req.destination,
        "status": status,
        "delay_mins": delay_mins,
        "reason": reason
    }
