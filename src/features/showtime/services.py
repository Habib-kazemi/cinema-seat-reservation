from datetime import date, timedelta
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.features.movie.schemas import MovieResponse
from src.features.movie.models import Movie
from .models import Showtime
from .schemas import ShowtimeCreate, ShowtimeResponse


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


def create_showtime(showtime: ShowtimeCreate, db: Session) -> ShowtimeResponse:
    # Check for duplicate showtime
    existing_showtime = db.query(Showtime).filter(
        Showtime.movie_id == showtime.movie_id,
        Showtime.hall_id == showtime.hall_id,
        Showtime.start_time == showtime.start_time
    ).first()
    if existing_showtime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Showtime with same movie, hall, and start time already exists"
        )

    # Validate end_time is after start_time and matches movie duration
    movie = db.query(Movie).filter(Movie.id == showtime.movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    # Calculate expected end_time based on movie duration
    expected_end_time = showtime.start_time + timedelta(minutes=movie.duration)
    if showtime.end_time <= showtime.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    if showtime.end_time != expected_end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"End time must match movie duration ({movie.duration} minutes)"
        )

    db_showtime = Showtime(**showtime.model_dump())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return ShowtimeResponse(
        id=db_showtime.id,
        movie_id=db_showtime.movie_id,
        hall_id=db_showtime.hall_id,
        start_time=db_showtime.start_time,
        end_time=db_showtime.end_time,
        price=db_showtime.price,
        movie=MovieResponse(
            id=movie.id,
            title=movie.title,
            genre_id=movie.genre_id,
            duration=movie.duration,
            release_date=movie.release_date,
            description=movie.description,
            poster_url=movie.poster_url
        )
    )
