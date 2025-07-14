from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from .services import get_showtimes, create_showtime, update_showtime, partial_update_showtime, delete_showtime
from .schemas import ShowtimeCreate, ShowtimeResponse
from datetime import date
from typing import Optional, List

router = APIRouter(tags=["showtime"])


@router.get("/", response_model=List[ShowtimeResponse])
async def get_showtimes_endpoint(
    movie_id: Optional[int] = None,
    showtime_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return get_showtimes(movie_id, showtime_date, db)


@router.post("/", response_model=ShowtimeResponse, status_code=201)
async def create_showtime_endpoint(showtime: ShowtimeCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    return create_showtime(showtime, db)


@router.put("/{showtime_id}", response_model=ShowtimeResponse)
async def update_showtime_endpoint(showtime_id: int, showtime: ShowtimeCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    return update_showtime(showtime_id, showtime, db)


@router.patch("/{showtime_id}", response_model=ShowtimeResponse)
async def partial_update_showtime_endpoint(
    showtime_id: int,
    movie_id: Optional[int] = None,
    hall_id: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    price: Optional[float] = None,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    return partial_update_showtime(showtime_id, movie_id, hall_id, start_time, end_time, price, db)


@router.delete("/{showtime_id}", response_model=dict)
async def delete_showtime_endpoint(showtime_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    return delete_showtime(showtime_id, db)
