"""
Movie-related API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Movie, Genre
from ..schemas import MovieCreate, MovieResponse

router = APIRouter(tags=["movies"])


@router.get("/", response_model=List[MovieResponse])
async def get_movies(db: Session = Depends(get_db)):
    """
    Get a list of all movies.
    """
    movies = db.query(Movie).all()
    return movies


@router.post("/", response_model=MovieResponse)
async def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """
    Add a new movie (admin only).
    """
    try:
        # Validate genre_id
        genre = db.query(Genre).filter(Genre.id == movie.genre_id).first()
        if not genre:
            raise HTTPException(status_code=400, detail="Invalid genre ID")

        db_movie = Movie(
            title=movie.title,
            genre_id=movie.genre_id,
            duration=movie.duration,
            release_date=movie.release_date,
            description=movie.description,
            poster_url=movie.poster_url
        )
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Internal server error") from exc
