"""
Admin-related API routes for managing movies and showtimes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import Movie, Showtime, User
from ..schemas import MovieCreate, MovieResponse, ShowtimeCreate, ShowtimeResponse

router = APIRouter(prefix="/admin", tags=["admin"])


def check_admin(user: User = Depends(get_current_user)):
    """
    Ensure the user has admin privileges.

    Args:
        user: Current user from authentication dependency.

    Returns:
        User: The authenticated admin user.

    Raises:
        HTTPException: If the user is not an admin.
    """
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


@router.post("/movies/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Create a new movie.

    Args:
        movie: Movie data to create.
        db: Database session.
        _: Admin user (unused, verified by check_admin).

    Returns:
        MovieResponse: Created movie details.
    """
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.delete("/movies/{movie_id}", response_model=dict)
async def delete_movie(movie_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Delete a movie by ID.

    Args:
        movie_id: ID of the movie to delete.
        db: Database session.
        _: Admin user (unused, verified by check_admin).

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the movie is not found.
    """
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}


@router.post("/showtimes/", response_model=ShowtimeResponse)
async def create_showtime(
    showtime: ShowtimeCreate, db: Session = Depends(get_db), _=Depends(check_admin)
):
    """
    Create a new showtime.

    Args:
        showtime: Showtime data to create.
        db: Database session.
        _: Admin user (unused, verified by check_admin).

    Returns:
        ShowtimeResponse: Created showtime details.
    """
    db_showtime = Showtime(**showtime.dict())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime


@router.delete("/showtimes/{showtime_id}", response_model=dict)
async def delete_showtime(showtime_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Delete a showtime by ID.

    Args:
        showtime_id: ID of the showtime to delete.
        db: Database session.
        _: Admin user (unused, verified by check_admin).

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the showtime is not found.
    """
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    db.delete(showtime)
    db.commit()
    return {"message": "Showtime deleted successfully"}
