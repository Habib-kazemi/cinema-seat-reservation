from sqlalchemy.orm import Session
from .models import Movie
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
