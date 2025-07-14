from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .models import Showtime
from .schemas import ShowtimeCreate, ShowtimeResponse
from datetime import date
from typing import Optional, List


def get_showtimes(movie_id: Optional[int], showtime_date: Optional[date], db: Session) -> List[Showtime]:
    query = db.query(Showtime)
    if movie_id:
        query = query.filter(Showtime.movie_id == movie_id)
    if showtime_date:
        query = query.filter(func.date(Showtime.start_time) == showtime_date)
    return query.all()


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
    db.delete(showtime)
    db.commit()
    return {"message": "Showtime deleted successfully"}
