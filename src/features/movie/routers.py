import logging
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from .services import get_movies
from .schemas import MovieResponse

router = APIRouter(tags=["movie"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[MovieResponse])
async def get_movies_endpoint(
    genre_id: Optional[int] = None,
    release_date_gte: Optional[date] = None,
    release_date_lte: Optional[date] = None,
    db: Session = Depends(get_db)
):
    {release_date_gte}, release_date_lte = {release_date_lte}")
    return get_movies(genre_id, release_date_gte, release_date_lte, db)
