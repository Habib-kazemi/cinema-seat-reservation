from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.features.cinema.models import Cinema
from src.features.hall.models import Hall
from src.features.movie.models import Movie
from src.features.showtime.models import Showtime
from src.features.users.models import User
from src.features.reservation.models import Reservation, Status
from src.features.cinema.schemas import CinemaCreate
from src.features.hall.schemas import HallCreate
from src.features.movie.schemas import MovieCreate
from src.features.showtime.schemas import ShowtimeCreate
from src.features.users.schemas import UserResponse
from src.features.reservation.schemas import ReservationResponse


def create_cinema(cinema: CinemaCreate, db: Session):
    db_cinema = Cinema(**cinema.model_dump())
    db.add(db_cinema)
    db.commit()
    db.refresh(db_cinema)
    return db_cinema


def update_cinema(cinema_id: int, cinema: CinemaCreate, db: Session):
    db_cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not db_cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    for key, value in cinema.model_dump().items():
        setattr(db_cinema, key, value)
    db.commit()
    db.refresh(db_cinema)
    return db_cinema


def partial_update_cinema(
    cinema_id: int,
    name: Optional[str],
    address: Optional[str],
    db: Session
):
    db_cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not db_cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    if name is not None:
        db_cinema.name = name
    if address is not None:
        db_cinema.address = address
    db.commit()
    db.refresh(db_cinema)
    return db_cinema


def delete_cinema(cinema_id: int, db: Session):
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    dependent_halls = db.query(Hall).filter(
        Hall.cinema_id == cinema_id).first()
    if dependent_halls:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete cinema because it has associated halls")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Deletion not allowed; please remove dependent halls first")


def create_hall(hall: HallCreate, db: Session):
    cinema = db.query(Cinema).filter(Cinema.id == hall.cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    if hall.rows <= 0 or hall.columns <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Rows and columns must be positive")
    db_hall = Hall(
        name=hall.name,
        rows=hall.rows,
        columns=hall.columns,
        cinema_id=hall.cinema_id
    )
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall


def update_hall(hall_id: int, hall: HallCreate, db: Session):
    db_hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not db_hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")
    cinema = db.query(Cinema).filter(Cinema.id == hall.cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    if hall.rows <= 0 or hall.columns <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Rows and columns must be positive")
    db_hall.name = hall.name
    db_hall.rows = hall.rows
    db_hall.columns = hall.columns
    db_hall.cinema_id = hall.cinema_id
    db.commit()
    db.refresh(db_hall)
    return db_hall


def partial_update_hall(
    hall_id: int,
    name: Optional[str],
    rows: Optional[int],
    columns: Optional[int],
    cinema_id: Optional[int],
    db: Session
):
    db_hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not db_hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")
    if name is not None:
        db_hall.name = name
    if rows is not None:
        if rows <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Rows must be positive")
        db_hall.rows = rows
    if columns is not None:
        if columns <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Columns must be positive")
        db_hall.columns = columns
    if cinema_id is not None:
        cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
        if not cinema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
        db_hall.cinema_id = cinema_id
    db.commit()
    db.refresh(db_hall)
    return db_hall


def delete_hall(hall_id: int, db: Session):
    hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")
    dependent_showtimes = db.query(Showtime).filter(
        Showtime.hall_id == hall_id).first()
    if dependent_showtimes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete hall because it has associated showtimes")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Deletion not allowed; please remove dependent showtimes first")


def create_movie(movie: MovieCreate, db: Session):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(movie_id: int, movie: MovieCreate, db: Session):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def partial_update_movie(
    movie_id: int,
    title: Optional[str],
    genre_id: Optional[int],
    duration: Optional[int],
    release_date: Optional[str],
    description: Optional[str],
    poster_url: Optional[str],
    db: Session
):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if title is not None:
        db_movie.title = title
    if genre_id is not None:
        db_movie.genre_id = genre_id
    if duration is not None:
        db_movie.duration = duration
    if release_date is not None:
        db_movie.release_date = release_date
    if description is not None:
        db_movie.description = description
    if poster_url is not None:
        db_movie.poster_url = poster_url
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(movie_id: int, db: Session):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    dependent_showtimes = db.query(Showtime).filter(
        Showtime.movie_id == movie_id).first()
    if dependent_showtimes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete movie because it has associated showtimes")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Deletion not allowed; please remove dependent showtimes first")


def create_showtime(showtime: ShowtimeCreate, db: Session):
    db_showtime = Showtime(**showtime.model_dump())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime


def update_showtime(showtime_id: int, showtime: ShowtimeCreate, db: Session):
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not db_showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    for key, value in showtime.model_dump().items():
        setattr(db_showtime, key, value)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime


def partial_update_showtime(
    showtime_id: int,
    movie_id: Optional[int],
    hall_id: Optional[int],
    start_time: Optional[str],
    end_time: Optional[str],
    price: Optional[float],
    db: Session
):
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not db_showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    if movie_id is not None:
        db_showtime.movie_id = movie_id
    if hall_id is not None:
        db_showtime.hall_id = hall_id
    if start_time is not None:
        db_showtime.start_time = start_time
    if end_time is not None:
        db_showtime.end_time = end_time
    if price is not None:
        db_showtime.price = price
    db.commit()
    db.refresh(db_showtime)
    return db_showtime


def delete_showtime(showtime_id: int, db: Session):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    dependent_reservations = db.query(Reservation).filter(
        Reservation.showtime_id == showtime_id).first()
    if dependent_reservations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete showtime because it has associated reservations")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Deletion not allowed; please remove dependent reservations first")


def get_users_with_reservations(db: Session) -> List[UserResponse]:
    users = db.query(User).join(Reservation, User.id ==
                                Reservation.user_id).distinct().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No user with reservation found")
    return users


def get_total_sales(
    db: Session,
    cinema_id: Optional[int] = None,
    showtime_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> dict:
    query = db.query(func.sum(Reservation.price)).filter(
        Reservation.status == Status.CONFIRMED
    )
    if cinema_id:
        query = query.join(Showtime, Reservation.showtime_id == Showtime.id
                           ).join(Hall, Showtime.hall_id == Hall.id
                                  ).filter(Hall.cinema_id == cinema_id)
        if not db.query(Cinema).filter(Cinema.id == cinema_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    if showtime_id:
        query = query.filter(Reservation.showtime_id == showtime_id)
        if not db.query(Showtime).filter(Showtime.id == showtime_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    if start_date:
        query = query.filter(Reservation.created_at >= start_date)
    if end_date:
        query = query.filter(Reservation.created_at <= end_date)
    total = query.scalar() or 0.0
    return {"total_sales": float(total)}


def approve_reservation(reservation_id: int, db: Session) -> ReservationResponse:
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.status == Status.CONFIRMED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Reservation already confirmed")
    reservation.status = Status.CONFIRMED
    db.commit()
    db.refresh(reservation)
    return reservation


def reject_reservation(reservation_id: int, db: Session) -> ReservationResponse:
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.status == Status.CANCELED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Reservation already canceled")
    reservation.status = Status.CANCELED
    db.commit()
    db.refresh(reservation)
    return reservation
