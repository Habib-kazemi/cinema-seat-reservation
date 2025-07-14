from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from src.features.cinema.schemas import CinemaCreate, CinemaResponse
from src.features.hall.schemas import HallCreate, HallResponse
from src.features.movie.schemas import MovieCreate, MovieResponse
from src.features.showtime.schemas import ShowtimeCreate, ShowtimeResponse
from src.features.users.schemas import UserResponse
from src.features.reservation.schemas import ReservationResponse
from .services import (
    create_cinema, delete_cinema, create_hall, update_hall, partial_update_hall, delete_hall,
    create_movie, update_movie, partial_update_movie, delete_movie,
    create_showtime, update_showtime, partial_update_showtime, delete_showtime,
    get_users_with_reservations
)

router = APIRouter(tags=["admin"], dependencies=[Depends(check_admin)])


@router.post("/cinema", response_model=CinemaResponse, status_code=status.HTTP_201_CREATED)
async def create_cinema_endpoint(cinema: CinemaCreate, db: Session = Depends(get_db)):
    return create_cinema(cinema, db)


@router.delete("/cinema/{cinema_id}", response_model=dict)
async def delete_cinema_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    return delete_cinema(cinema_id, db)


@router.post("/hall", response_model=HallResponse, status_code=status.HTTP_201_CREATED)
async def create_hall_endpoint(hall: HallCreate, db: Session = Depends(get_db)):
    return create_hall(hall, db)


@router.put("/hall/{hall_id}", response_model=HallResponse)
async def update_hall_endpoint(hall_id: int, hall: HallCreate, db: Session = Depends(get_db)):
    return update_hall(hall_id, hall, db)


@router.patch("/hall/{hall_id}", response_model=HallResponse)
async def partial_update_hall_endpoint(
    hall_id: int,
    name: Optional[str] = None,
    rows: Optional[int] = None,
    columns: Optional[int] = None,
    cinema_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return partial_update_hall(hall_id, name, rows, columns, cinema_id, db)


@router.delete("/hall/{hall_id}", response_model=dict)
async def delete_hall_endpoint(hall_id: int, db: Session = Depends(get_db)):
    return delete_hall(hall_id, db)


@router.post("/movie", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie_endpoint(movie: MovieCreate, db: Session = Depends(get_db)):
    return create_movie(movie, db)


@router.put("/movie/{movie_id}", response_model=MovieResponse)
async def update_movie_endpoint(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    return update_movie(movie_id, movie, db)


@router.patch("/movie/{movie_id}", response_model=MovieResponse)
async def partial_update_movie_endpoint(
    movie_id: int,
    title: Optional[str] = None,
    genre_id: Optional[int] = None,
    duration: Optional[int] = None,
    release_date: Optional[str] = None,
    description: Optional[str] = None,
    poster_url: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return partial_update_movie(movie_id, title, genre_id, duration, release_date, description, poster_url, db)


@router.delete("/movie/{movie_id}", response_model=dict)
async def delete_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    return delete_movie(movie_id, db)


@router.post("/showtime", response_model=ShowtimeResponse, status_code=status.HTTP_201_CREATED)
async def create_showtime_endpoint(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    return create_showtime(showtime, db)


@router.put("/showtime/{showtime_id}", response_model=ShowtimeResponse)
async def update_showtime_endpoint(showtime_id: int, showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    return update_showtime(showtime_id, showtime, db)


@router.patch("/showtime/{showtime_id}", response_model=ShowtimeResponse)
async def partial_update_showtime_endpoint(
    showtime_id: int,
    movie_id: Optional[int] = None,
    hall_id: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    return partial_update_showtime(showtime_id, movie_id, hall_id, start_time, end_time, price, db)


@router.delete("/showtime/{showtime_id}", response_model=dict)
async def delete_showtime_endpoint(showtime_id: int, db: Session = Depends(get_db)):
    return delete_showtime(showtime_id, db)


@router.get("/users", response_model=List[UserResponse])
async def get_users_with_reservations_endpoint(db: Session = Depends(get_db)):
    return get_users_with_reservations(db)


@router.post("/reservation/{reservation_id}/approve", response_model=ReservationResponse)
async def approve_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    return approve_reservation(reservation_id, db)


@router.post("/reservation/{reservation_id}/reject", response_model=ReservationResponse)
async def reject_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    return reject_reservation(reservation_id, db)
