from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PackingRequest(BaseModel):
    city: str
    trip_days: int
    month: int
    activities: str | None = None

@router.post("/packing")
def packing(req: PackingRequest):
    items = []
    items.append({"item": "T-shirt", "quantity": max(3, req.trip_days)})
    items.append({"item": "Pants/Jeans", "quantity": max(2, req.trip_days // 2)})

    if req.month in (12, 1, 2):
        items.append({"item": "Jacket", "quantity": 1})

    acts = (req.activities or "").lower()
    if "beach" in acts:
        items.append({"item": "Swimwear", "quantity": 1})
        items.append({"item": "Sunscreen", "quantity": 1})
        items.append({"item": "Flip-flops", "quantity": 1})

    return {"city": req.city, "items": items}
