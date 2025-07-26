import logging
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from .services import get_showtimes
from .schemas import ShowtimeResponse

router = APIRouter(tags=["showtime"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[ShowtimeResponse])
async def get_showtimes_endpoint(
    movie_id: Optional[int] = None,
    showtime_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    logger.info(
        f"Fetching showtimes with filters: movie_id={movie_id}, showtime_date={showtime_date}")
    return get_showtimes(movie_id, showtime_date, db)
