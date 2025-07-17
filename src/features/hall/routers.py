from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from .services import get_hall_with_showtimes
from .schemas import HallResponse
from typing import List

router = APIRouter(tags=["hall"])


@router.get("/{cinema_id}/hall", response_model=List[HallResponse])
async def get_hall_with_showtimes_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    return get_hall_with_showtimes(cinema_id, db)
