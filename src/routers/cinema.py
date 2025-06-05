"""
Cinema-related API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cinema, Hall, Showtime, Movie, User
from ..schemas import CinemaCreate, CinemaResponse, HallResponse, ShowtimeResponse
from .auth import get_current_user

router = APIRouter(tags=["cinema"])


@router.post("/", response_model=CinemaResponse, status_code=status.HTTP_201_CREATED)
async def create_cinema(
    cinema: CinemaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new cinema.

    Args:
        cinema: Cinema data to create.
        db: Database session.
        current_user: Authenticated user (must be admin).

    Returns:
        Created cinema details.

    Raises:
        HTTPException: If user is not admin or cinema name already exists.
    """
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    existing_cinema = db.query(Cinema).filter(
        Cinema.name == cinema.name).first()
    if existing_cinema:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cinema name already exists")
    db_cinema = Cinema(**cinema.dict())
    db.add(db_cinema)
    db.commit()
    db.refresh(db_cinema)
    return db_cinema


@router.get("/", response_model=List[CinemaResponse])
async def get_cinemas(
        db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all cinemas.

    Args:
        db: Database session.
        current_user: Authenticated user.

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


@router.get("/{cinema_id}", response_model=CinemaResponse)
async def get_cinema(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific cinema by ID.

    Args:
        cinema_id: ID of the cinema.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        Cinema details with associated halls.

    Raises:
        HTTPException: If cinema is not found.
    """
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    return cinema


@router.get("/{cinema_id}/halls", response_model=List[HallResponse])
async def get_cinema_halls(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all halls for a specific cinema.

    Args:
        cinema_id: ID of the cinema.
        db: Database session.
        current_user: Authenticated user.

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
async def get_cinema_showtimes(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all showtimes for a specific cinema.

    Args:
        cinema_id: ID of the cinema.
        db: Database session.
        current_user: Authenticated user.

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


@router.delete("/{cinema_id}", response_model=dict)
async def delete_cinema(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a cinema by ID.

    Args:
        cinema_id: ID of the cinema.
        db: Database session.
        current_user: Authenticated user (must be admin).

    Returns:
        Confirmation message.

    Raises:
        HTTPException: If user is not admin or cinema is not found.
    """
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    db.delete(cinema)
    db.commit()
    return {"message": "Cinema deleted successfully"}
