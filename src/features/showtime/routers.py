from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from .services import get_showtimes
from .schemas import ShowtimeResponse
from datetime import date
from typing import Optional, List

router = APIRouter(tags=["showtime"])


@router.get("/", response_model=List[ShowtimeResponse])
async def get_showtimes_endpoint(
    movie_id: Optional[int] = None,
    showtime_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return get_showtimes(movie_id, showtime_date, db)
