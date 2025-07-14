from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from .services import get_movies, create_movie, update_movie, partial_update_movie, delete_movie
from .schemas import MovieCreate, MovieResponse

router = APIRouter(tags=["movie"])


@router.get("/", response_model=List[MovieResponse])
async def get_movies_endpoint(
    genre_id: Optional[int] = None,
    release_date_gte: Optional[date] = None,
    release_date_lte: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return get_movies(genre_id, release_date_gte, release_date_lte, db)


@router.post("/", response_model=MovieResponse, status_code=201)
async def create_movie_endpoint(movie: MovieCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    return create_movie(movie, db)


@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie_endpoint(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    return update_movie(movie_id, movie, db)


@router.patch("/{movie_id}", response_model=MovieResponse)
async def partial_update_movie_endpoint(
    movie_id: int,
    title: Optional[str] = None,
    genre_id: Optional[int] = None,
    duration: Optional[int] = None,
    release_date: Optional[str] = None,
    description: Optional[str] = None,
    poster_url: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    return partial_update_movie(movie_id, title, genre_id, duration, release_date, description, poster_url, db)


@router.delete("/{movie_id}", response_model=dict)
async def delete_movie_endpoint(movie_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    return delete_movie(movie_id, db)
