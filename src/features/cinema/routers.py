import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
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
    try:
        logger.info("Fetching all cinemas")
        result = get_cinemas(db)
        logger.info("Fetched %s cinemas", len(result))
        return result
    except HTTPException as e:
        logger.error("Failed to fetch cinemas, error: %s", str(e.detail))
        raise
    except Exception as e:
        logger.error("Unexpected error fetching cinemas, error: %s", str(e))
        raise


@router.get("/{cinema_id}/hall", response_model=List[HallResponse])
async def get_cinema_halls_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Fetching halls for cinema ID: %s", cinema_id)
        result = get_cinema_halls(cinema_id, db)
        logger.info("Fetched %s halls for cinema ID: %s",
                    len(result), cinema_id)
        return result
    except HTTPException as e:
        logger.error(
            "Failed to fetch halls for cinema ID: %s, error: %s", cinema_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error fetching halls for cinema ID: %s, error: %s", cinema_id, str(e))
        raise


@router.get("/{cinema_id}/showtime", response_model=List[ShowtimeResponse])
async def get_cinema_showtimes_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Fetching showtimes for cinema ID: %s", cinema_id)
        result = get_cinema_showtimes(cinema_id, db)
        logger.info("Fetched %s showtimes for cinema ID: %s",
                    len(result), cinema_id)
        return result
    except HTTPException as e:
        logger.error(
            "Failed to fetch showtimes for cinema ID: %s, error: %s", cinema_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error fetching showtimes for cinema ID: %s, error: %s", cinema_id, str(e))
        raise
