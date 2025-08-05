import logging
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
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
    try:
        logger.info(
            "Fetching showtimes with filters: movie_id=%s, showtime_date=%s", movie_id, showtime_date)
        result = get_showtimes(movie_id, showtime_date, db)
        logger.info("Fetched %s showtimes", len(result))
        return result
    except HTTPException as e:
        logger.error("Failed to fetch showtimes with filters: movie_id=%s, showtime_date=%s, error: %s",
                     movie_id, showtime_date, str(e.detail))
        raise
    except Exception as e:
        logger.error("Unexpected error fetching showtimes with filters: movie_id=%s, showtime_date=%s, error: %s",
                     movie_id, showtime_date, str(e))
        raise
