import logging
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from .services import get_hall_with_showtimes
from .schemas import HallResponse

router = APIRouter(tags=["hall"])
logger = logging.getLogger(__name__)


@router.get("/{cinema_id}/hall", response_model=List[HallResponse])
async def get_hall_with_showtimes_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    logger.info("Fetching halls with showtimes for cinema ID: %s", cinema_id)
    result = get_hall_with_showtimes(cinema_id, db)
    logger.info("Fetched %s halls with showtimes for cinema ID: %s",
                len(result), cinema_id)
    return result
