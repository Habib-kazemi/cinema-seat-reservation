"""
Cinema-related API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cinema, Hall, Showtime, Movie
from ..schemas import CinemaResponse, HallResponse, ShowtimeResponse

router = APIRouter(tags=["cinema"])


@router.get("/", response_model=List[CinemaResponse])
async def get_cinemas(db: Session = Depends(get_db)):
    """
    Get all cinemas.

    Args:
        db: Database session.

    Returns:
        List of all cinemas with their halls.

    Raises:
        HTTPException: If no cinemas are found.
    """
    cinemas = db.query(Cinema).all()
    if not cinemas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No cinemas found")
    return cinemas


@router.get("/{cinema_id}/halls", response_model=List[HallResponse])
async def get_cinema_halls(cinema_id: int, db: Session = Depends(get_db)):
    """
    Get all halls for a specific cinema.

    Args:
        cinema_id: ID of the cinema.
        db: Database session.

    Returns:
        List of halls in the specified cinema.

    Raises:
        HTTPException: If cinema or halls are not found.
    """
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    halls = db.query(Hall).filter(Hall.cinema_id == cinema_id).all()
    if not halls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No halls found for this cinema")
    return halls


@router.get("/{cinema_id}/showtimes", response_model=List[ShowtimeResponse])
async def get_cinema_showtimes(cinema_id: int, db: Session = Depends(get_db)):
    """
    Get all showtimes for a specific cinema.

    Args:
        cinema_id: ID of the cinema.
        db: Database session.

    Returns:
        List of showtimes with movie and hall details for the specified cinema.

    Raises:
        HTTPException: If cinema or showtimes are not found.
    """
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    showtimes = db.query(Showtime).join(Hall).filter(
        Hall.cinema_id == cinema_id).join(Movie).all()
    if not showtimes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No showtimes found for this cinema")
    return showtimes
