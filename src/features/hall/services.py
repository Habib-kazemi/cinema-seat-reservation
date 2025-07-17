from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.features.cinema.models import Cinema
from .models import Hall
from .schemas import HallResponse


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
