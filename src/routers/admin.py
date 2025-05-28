"""
Admin-related API routes for managing movies, showtimes, and halls.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import Hall, Movie, Showtime, User
from ..schemas import HallCreate, HallResponse, MovieCreate, MovieResponse, ShowtimeCreate, ShowtimeResponse

router = APIRouter(tags=["admin"])


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


@router.get("/halls", response_model=List[HallResponse])
async def get_halls(db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Retrieve a list of all cinema halls.

    Args:
        db: Database session.
        _: Admin user.

    Returns:
        List[HallResponse]: List of all halls with their details.
    """
    halls = db.query(Hall).all()
    return halls


@router.post("/halls", response_model=HallResponse)
async def create_hall(hall: HallCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Create a new cinema hall.

    Args:
        hall: Hall data including name, rows, and columns.
        db: Database session.
        _: Admin user.

    Returns:
        HallResponse: Created hall details.

    Raises:
        HTTPException: If rows or columns are invalid.
    """
    try:
        # Check if rows and columns are positive
        if hall.rows <= 0 or hall.columns <= 0:
            raise HTTPException(
                status_code=400, detail="Rows and columns must be positive")

        # Create new hall
        db_hall = Hall(
            name=hall.name,
            rows=hall.rows,
            columns=hall.columns
        )
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)

        return db_hall

    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Internal server error") from exc


@router.delete("/halls/{hall_id}", response_model=dict)
async def delete_hall(hall_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Delete a cinema hall by ID.

    Args:
        hall_id: ID of the hall to delete.
        db: Database session.
        _: Admin user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the hall is not found.
    """
    hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")
    db.delete(hall)
    db.commit()
    return {"message": "Hall deleted successfully"}


@router.post("/movies", response_model=MovieResponse)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Create a new movie.

    Args:
        movie: Movie data to create.
        db: Database session.
        _: Admin user.

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
        _: Admin user.

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


@router.post("/showtimes", response_model=ShowtimeResponse)
async def create_showtime(
    showtime: ShowtimeCreate, db: Session = Depends(get_db), _=Depends(check_admin)
):
    """
    Create a new showtime.

    Args:
        showtime: Showtime data to create.
        db: Database session.
        _: Admin user.

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
        _: Admin user.

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
