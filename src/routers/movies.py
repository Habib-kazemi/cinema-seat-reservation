
"""
Movie-related API routes
"""
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Movie
from ..schemas import MovieResponse

router = APIRouter(tags=["movies"])


@router.get("/", response_model=List[MovieResponse])
async def get_movies(
    genre_id: Optional[int] = None,
    release_date_gte: Optional[date] = None,
    release_date_lte: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of movies with optional filters.

    Args:
        genre_id: Filter by genre ID.
        release_date_gte: Filter by release date greater than or equal to (YYYY-MM-DD).
        release_date_lte: Filter by release date less than or equal to (YYYY-MM-DD).
        db: Database session.

    Returns:
        List of movies matching the filters.
    """
    query = db.query(Movie)
    if genre_id:
        query = query.filter(Movie.genre_id == genre_id)
    if release_date_gte:
        query = query.filter(Movie.release_date >= release_date_gte)
    if release_date_lte:
        query = query.filter(Movie.release_date <= release_date_lte)
    return query.all()
