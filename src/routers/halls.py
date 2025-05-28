"""
Hall-related API routes for public access.
"""
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Hall, Showtime
from ..schemas import HallShowtimeResponse

router = APIRouter(tags=["halls"])


@router.get("/", response_model=List[HallShowtimeResponse])
async def get_halls_with_showtimes(db: Session = Depends(get_db)):
    """
    Retrieve a list of all cinema halls with their current showtimes and movies.

    Args:
        db: Database session.

    Returns:
        List[HallShowtimeResponse]: List of halls with their active showtimes and movie details.
    """
    current_time = datetime.now(timezone.utc)
    halls = db.query(Hall).all()
    result = []
    for hall in halls:
        showtimes = db.query(Showtime).filter(
            Showtime.hall_id == hall.id,
            Showtime.start_time <= current_time,
            Showtime.end_time >= current_time
        ).all()
        showtime_data = [
            {
                "id": showtime.id,
                "movie": {
                    "id": showtime.movie.id,
                    "title": showtime.movie.title
                },
                "start_time": showtime.start_time,
                "end_time": showtime.end_time,
                "price": showtime.price
            }
            for showtime in showtimes
        ]
        result.append({
            "id": hall.id,
            "name": hall.name,
            "rows": hall.rows,
            "columns": hall.columns,
            "showtimes": showtime_data
        })
    return result
