from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone

# ✅ This must exist, or main.py can't do payments.router
router = APIRouter()

class PaymentRequest(BaseModel):
    user_id: int | None = None
    amount: float
    currency: str = "INR"

@router.post("/mock_checkout")
def mock_checkout(req: PaymentRequest):
    tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    return {
        "status": "success",
        "transaction_id": tx_id,
        "amount": req.amount,
        "currency": req.currency,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
