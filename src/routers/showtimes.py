
"""
Showtime-related API routes
"""
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from ..database import get_db
from ..models import Showtime
from ..schemas import ShowtimeResponse

router = APIRouter(tags=["showtimes"])


@router.get("/", response_model=List[ShowtimeResponse])
async def get_showtimes(
    movie_id: Optional[int] = None,
    showtime_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of showtimes with optional filters.

    Args:
        movie_id: Filter by movie ID.
        showtime_date: Filter by showtime date (YYYY-MM-DD).
        db: Database session.

    Returns:
        List of showtimes matching the filters.
    """
    query = db.query(Showtime)
    if movie_id:
        query = query.filter(Showtime.movie_id == movie_id)
    if showtime_date:
        query = query.filter(func.date(Showtime.start_time) == showtime_date)
    return query.all()
