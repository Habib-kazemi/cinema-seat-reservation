import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.database import get_db
from .services import get_hall_with_showtimes
from .schemas import HallResponse

router = APIRouter(tags=["hall"])
logger = logging.getLogger(__name__)


@router.get("/hall", response_model=List[HallResponse])
async def get_hall_with_showtimes_endpoint(cinema_id: Optional[int] = Query(None, description="Filter by cinema ID"), db: Session = Depends(get_db)):
    try:
        logger.info(
            "Fetching halls with showtimes for cinema ID: %s", cinema_id if cinema_id else "all")
        result = get_hall_with_showtimes(db, cinema_id)
        logger.info("Fetched %s halls with showtimes for cinema ID: %s", len(
            result), cinema_id if cinema_id else "all")
        return result
    except HTTPException as e:
        logger.error(
            "Failed to fetch halls with showtimes for cinema ID: %s, error: %s", cinema_id if cinema_id else "all", str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error fetching halls with showtimes for cinema ID: %s, error: %s", cinema_id if cinema_id else "all", str(e))
        raise
