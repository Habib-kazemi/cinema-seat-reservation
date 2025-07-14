# Placeholder for payment logic
from fastapi import HTTPException


def initiate_payment(amount: float, reservation_id: int, callback_url: str):
    raise HTTPException(
        status_code=501, detail="Payment integration not implemented")
