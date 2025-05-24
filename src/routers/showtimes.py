"""
Showtime-related API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Showtime, Movie, Hall
from ..schemas import ShowtimeCreate, ShowtimeResponse

router = APIRouter(tags=["showtimes"])


@router.get("/", response_model=List[ShowtimeResponse])
async def get_showtimes(db: Session = Depends(get_db)):
    """
    Get a list of all showtimes.
    """
    showtimes = db.query(Showtime).all()
    return showtimes


@router.post("/", response_model=ShowtimeResponse)
async def create_showtime(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    """
    Create a new showtime for a movie in a hall.

    Args:
        showtime: Showtime data including movie_id, hall_id, start_time, end_time, and price.
        db: Database session.

    Returns:
        ShowtimeResponse: Created showtime details.

    Raises:
        HTTPException: If movie, hall, or time is invalid.
    """
    try:
        # Check if movie exists
        movie = db.query(Movie).filter(Movie.id == showtime.movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # Check if hall exists
        hall = db.query(Hall).filter(Hall.id == showtime.hall_id).first()
        if not hall:
            raise HTTPException(status_code=404, detail="Hall not found")

        # Check if end_time is after start_time
        if showtime.end_time <= showtime.start_time:
            raise HTTPException(
                status_code=400, detail="End time must be after start time")

        # Create new showtime
        db_showtime = Showtime(
            movie_id=showtime.movie_id,
            hall_id=showtime.hall_id,
            start_time=showtime.start_time,
            end_time=showtime.end_time,
            price=showtime.price
        )
        db.add(db_showtime)
        db.commit()
        db.refresh(db_showtime)
        return db_showtime
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Internal server error") from exc
