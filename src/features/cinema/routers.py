import logging
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.features.hall.schemas import HallResponse
from src.features.showtime.schemas import ShowtimeResponse
from src.database import get_db
from .services import get_cinemas, get_cinema_halls, get_cinema_showtimes
from .schemas import CinemaResponse

router = APIRouter(tags=["cinema"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[CinemaResponse])
async def get_cinemas_endpoint(db: Session = Depends(get_db)):
    logger.info("Fetching all cinemas")
    return get_cinemas(db)


@router.get("/{cinema_id}/halls", response_model=List[HallResponse])
async def get_cinema_halls_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching halls for cinema ID: {cinema_id}")
    return get_cinema_halls(cinema_id, db)


@router.get("/{cinema_id}/showtimes", response_model=List[ShowtimeResponse])
async def get_cinema_showtimes_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching showtimes for cinema ID: {cinema_id}")
    return get_cinema_showtimes(cinema_id, db)
