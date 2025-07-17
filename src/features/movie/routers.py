from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from .services import get_movies
from .schemas import MovieResponse

router = APIRouter(tags=["movie"])


@router.get("/", response_model=List[MovieResponse])
async def get_movies_endpoint(
    genre_id: Optional[int] = None,
    release_date_gte: Optional[date] = None,
    release_date_lte: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return get_movies(genre_id, release_date_gte, release_date_lte, db)
