from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ItineraryRequest(BaseModel):
    city: str
    trip_days: int
    preferences: str | None = None

@router.post("/itinerary")
def build_itinerary(req: ItineraryRequest):
    days = []
    for d in range(1, req.trip_days + 1):
        days.append({
            "day": d,
            "items": [
                {"time": "Morning", "activity": f"Explore {req.city} - sightseeing"},
                {"time": "Afternoon", "activity": "Local food & markets"},
                {"time": "Evening", "activity": "Relax / optional activity"},
            ]
        })
    return {
        "city": req.city,
        "trip_days": req.trip_days,
        "itinerary": days
    }
