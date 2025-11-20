from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

KG_CO2_PER_KM = 0.115

class CarbonRequest(BaseModel):
    distance_km: float
    passengers: int = 1

@router.post("/carbon_footprint")
def carbon(req: CarbonRequest):
    total = req.distance_km * KG_CO2_PER_KM * req.passengers
    per_person = total / req.passengers
    return {
        "distance_km": req.distance_km,
        "passengers": req.passengers,
        "total_co2_kg": round(total, 2),
        "per_person_kg": round(per_person, 2),
    }
