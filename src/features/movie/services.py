from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import Movie
from .schemas import MovieCreate, MovieResponse
from datetime import date
from typing import Optional


def get_movies(genre_id: Optional[int], release_date_gte: Optional[date], release_date_lte: Optional[date], db: Session):
    query = db.query(Movie)
    if genre_id:
        query = query.filter(Movie.genre_id == genre_id)
    if release_date_gte:
        query = query.filter(Movie.release_date >= release_date_gte)
    if release_date_lte:
        query = query.filter(Movie.release_date <= release_date_lte)
    return query.all()


def create_movie(movie: MovieCreate, db: Session):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(movie_id: int, movie: MovieCreate, db: Session):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def partial_update_movie(
    movie_id: int,
    title: Optional[str],
    genre_id: Optional[int],
    duration: Optional[int],
    release_date: Optional[str],
    description: Optional[str],
    poster_url: Optional[str],
    db: Session
):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if title is not None:
        db_movie.title = title
    if genre_id is not None:
        db_movie.genre_id = genre_id
    if duration is not None:
        db_movie.duration = duration
    if release_date is not None:
        db_movie.release_date = release_date
    if description is not None:
        db_movie.description = description
    if poster_url is not None:
        db_movie.poster_url = poster_url
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(movie_id: int, db: Session):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}
