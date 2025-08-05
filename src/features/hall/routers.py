import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from .services import get_hall_with_showtimes
from .schemas import HallResponse

router = APIRouter(tags=["hall"])
logger = logging.getLogger(__name__)


@router.get("/{cinema_id}/hall", response_model=List[HallResponse])
async def get_hall_with_showtimes_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(
            "Fetching halls with showtimes for cinema ID: %s", cinema_id)
        result = get_hall_with_showtimes(cinema_id, db)
        logger.info("Fetched %s halls with showtimes for cinema ID: %s", len(
            result), cinema_id)
        return result
    except HTTPException as e:
        logger.error(
            "Failed to fetch halls with showtimes for cinema ID: %s, error: %s", cinema_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error fetching halls with showtimes for cinema ID: %s, error: %s", cinema_id, str(e))
        raise
