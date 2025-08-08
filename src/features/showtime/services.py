from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.features.movie.schemas import MovieResponse
from .models import Showtime
from .schemas import ShowtimeResponse


def get_showtimes(movie_id: Optional[int], showtime_date: Optional[date], db: Session) -> List[ShowtimeResponse]:
    query = db.query(Showtime)
    if movie_id:
        query = query.filter(Showtime.movie_id == movie_id)
    if showtime_date:
        query = query.filter(func.date(Showtime.start_time) == showtime_date)
    showtimes = query.all()
    return [ShowtimeResponse(
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
    ) for showtime in showtimes]
