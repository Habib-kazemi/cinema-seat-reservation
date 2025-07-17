from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.features.hall.models import Hall
from src.features.showtime.models import Showtime
from src.features.movie.models import Movie
from .models import Cinema
from .schemas import CinemaResponse


def get_cinemas(db: Session) -> List[CinemaResponse]:
    cinemas = db.query(Cinema).all()
    if not cinemas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No cinemas found")
    return cinemas


def get_cinema_halls(cinema_id: int, db: Session):
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    halls = db.query(Hall).filter(Hall.cinema_id == cinema_id).all()
    if not halls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No halls found for this cinema")
    return halls


def get_cinema_showtimes(cinema_id: int, db: Session):
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    showtimes = db.query(Showtime).join(Hall).filter(
        Hall.cinema_id == cinema_id).join(Movie).all()
    if not showtimes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No showtimes found for this cinema")
    return showtimes
