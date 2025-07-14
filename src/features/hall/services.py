from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import Hall
from .schemas import HallCreate, HallResponse
from src.features.cinema.models import Cinema
from datetime import datetime, timezone
from typing import Optional, List


def get_hall_with_showtimes(cinema_id: int, db: Session) -> List[HallResponse]:
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    halls = db.query(Hall).filter(Hall.cinema_id == cinema_id).all()
    if not halls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No hall found for this cinema")
    result = []
    current_time = datetime.now(timezone.utc)
    for hall in halls:
        showtimes = db.query(Showtime).filter(
            Showtime.hall_id == hall.id,
            Showtime.start_time >= current_time
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
    db.delete(hall)
    db.commit()
    return {"message": "Hall deleted successfully"}
