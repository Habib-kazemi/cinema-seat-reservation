"""
Hall-related API routes for public access.
"""
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import Hall, Showtime, Cinema, User
from ..schemas import HallResponse, ShowtimeResponse

router = APIRouter(tags=["hall"])


@router.get("/{cinema_id}/hall", response_model=List[HallResponse])
async def get_hall_with_showtimes(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a list of all cinema hall for a specific cinema with their current showtimes
    and movies.

    Args:
        cinema_id: ID of the cinema.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        List[HallResponse]: List of hall with their active showtimes and movie details.

    Raises:
        HTTPException: If cinema or hall are not found.
    """
    # Check if cinema exists
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")

    current_time = datetime.now(timezone.utc)
    halls = db.query(Hall).filter(Hall.cinema_id == cinema_id).all()
    if not halls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No hall found for this cinema")

    result = []
    for hall in halls:
        showtimes = db.query(Showtime).filter(
            Showtime.hall_id == hall.id,
            Showtime.start_time <= current_time,
            Showtime.end_time >= current_time
        ).all()
        hall_data = HallResponse(
            id=hall.id,
            name=hall.name,
            rows=hall.rows,
            columns=hall.columns,
            cinema_id=hall.cinema_id,
            showtimes=[
                ShowtimeResponse(
                    id=showtime.id,
                    movie_id=showtime.movie_id,
                    hall_id=showtime.hall_id,
                    start_time=showtime.start_time,
                    end_time=showtime.end_time,
                    price=showtime.price,
                    movie={
                        "id": showtime.movie.id,
                        "title": showtime.movie.title
                    }
                )
                for showtime in showtimes
            ]
        )
        result.append(hall_data)
    return result
