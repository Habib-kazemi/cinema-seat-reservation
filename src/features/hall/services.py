from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.features.cinema.models import Cinema
from src.features.showtime.models import Showtime
from src.features.showtime.schemas import ShowtimeResponse
from src.features.movie.schemas import MovieResponse
from .models import Hall
from .schemas import HallResponse


def get_hall_with_showtimes(db: Session, cinema_id: Optional[int] = None) -> List[HallResponse]:
    query = db.query(Hall)
    if cinema_id:
        query = query.filter(Hall.cinema_id == cinema_id)
        if not db.query(Cinema).filter(Cinema.id == cinema_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    halls = query.all()
    if not halls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No hall found")

    current_time = datetime.now(timezone.utc)
    return [HallResponse(
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
                movie=MovieResponse(
                    id=showtime.movie.id,
                    title=showtime.movie.title,
                    genre_id=showtime.movie.genre_id,
                    duration=showtime.movie.duration,
                    release_date=showtime.movie.release_date,
                    description=showtime.movie.description,
                    poster_url=showtime.movie.poster_url
                )
            )
            for showtime in db.query(Showtime)
            .filter(Showtime.hall_id == hall.id, Showtime.start_time >= current_time)
            .all()
        ]
    ) for hall in halls]
