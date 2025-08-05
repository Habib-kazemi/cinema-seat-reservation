import logging
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from src.features.cinema.schemas import CinemaCreate, CinemaResponse
from src.features.hall.schemas import HallCreate, HallResponse
from src.features.movie.schemas import MovieCreate, MovieResponse
from src.features.showtime.schemas import ShowtimeCreate, ShowtimeResponse
from src.features.users.schemas import UserResponse
from src.features.reservation.schemas import ReservationResponse
from .services import (
    create_cinema, delete_cinema, update_cinema, partial_update_cinema,
    create_hall, update_hall, partial_update_hall, delete_hall,
    create_movie, update_movie, partial_update_movie, delete_movie,
    create_showtime, update_showtime, partial_update_showtime, delete_showtime,
    get_users_with_reservations, approve_reservation, reject_reservation,
    get_total_sales
)

router = APIRouter(tags=["admin"], dependencies=[Depends(check_admin)])
logger = logging.getLogger(__name__)


@router.post("/cinema", response_model=CinemaResponse, status_code=status.HTTP_201_CREATED)
async def create_cinema_endpoint(cinema: CinemaCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Creating cinema: %s", cinema.name)
        result = create_cinema(cinema, db)
        logger.info("Created cinema with ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to create cinema: %s, error: %s",
                     cinema.name, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error creating cinema: %s, error: %s", cinema.name, str(e))
        raise


@router.put("/cinema/{cinema_id}", response_model=CinemaResponse)
async def update_cinema_endpoint(cinema_id: int, cinema: CinemaCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Updating cinema ID: %s", cinema_id)
        result = update_cinema(cinema_id, cinema, db)
        logger.info("Updated cinema ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to update cinema ID: %s, error: %s",
                     cinema_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error updating cinema ID: %s, error: %s", cinema_id, str(e))
        raise


@router.patch("/cinema/{cinema_id}", response_model=CinemaResponse)
async def partial_update_cinema_endpoint(
    cinema_id: int,
    name: Optional[str] = None,
    address: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        logger.info(
            "Partially updating cinema ID: %s with name: %s, address: %s", cinema_id, name, address)
        result = partial_update_cinema(cinema_id, name, address, db)
        logger.info("Partially updated cinema ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error(
            "Failed to partially update cinema ID: %s, error: %s", cinema_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error partially updating cinema ID: %s, error: %s", cinema_id, str(e))
        raise


@router.delete("/cinema/{cinema_id}", response_model=dict)
async def delete_cinema_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Deleting cinema ID: %s", cinema_id)
        delete_cinema(cinema_id, db)
        logger.info("Deleted cinema ID: %s", cinema_id)
        return {"message": f"Cinema {cinema_id} deleted successfully"}
    except HTTPException as e:
        logger.error("Failed to delete cinema ID: %s, error: %s",
                     cinema_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error deleting cinema ID: %s, error: %s", cinema_id, str(e))
        raise


@router.post("/hall", response_model=HallResponse, status_code=status.HTTP_201_CREATED)
async def create_hall_endpoint(hall: HallCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Creating hall: %s for cinema ID: %s",
                    hall.name, hall.cinema_id)
        result = create_hall(hall, db)
        logger.info("Created hall with ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to create hall: %s, error: %s",
                     hall.name, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error creating hall: %s, error: %s", hall.name, str(e))
        raise


@router.put("/hall/{hall_id}", response_model=HallResponse)
async def update_hall_endpoint(hall_id: int, hall: HallCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Updating hall ID: %s", hall_id)
        result = update_hall(hall_id, hall, db)
        logger.info("Updated hall ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to update hall ID: %s, error: %s",
                     hall_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error updating hall ID: %s, error: %s", hall_id, str(e))
        raise


@router.patch("/hall/{hall_id}", response_model=HallResponse)
async def partial_update_hall_endpoint(
    hall_id: int,
    name: Optional[str] = None,
    rows: Optional[int] = None,
    columns: Optional[int] = None,
    cinema_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        logger.info("Partially updating hall ID: %s with name: %s, rows: %s, columns: %s, cinema_id: %s",
                    hall_id, name, rows, columns, cinema_id)
        result = partial_update_hall(
            hall_id, name, rows, columns, cinema_id, db)
        logger.info("Partially updated hall ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error(
            "Failed to partially update hall ID: %s, error: %s", hall_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error partially updating hall ID: %s, error: %s", hall_id, str(e))
        raise


@router.delete("/hall/{hall_id}", response_model=dict)
async def delete_hall_endpoint(hall_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Deleting hall ID: %s", hall_id)
        delete_hall(hall_id, db)
        logger.info("Deleted hall ID: %s", hall_id)
        return {"message": f"Hall {hall_id} deleted successfully"}
    except HTTPException as e:
        logger.error("Failed to delete hall ID: %s, error: %s",
                     hall_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error deleting hall ID: %s, error: %s", hall_id, str(e))
        raise


@router.post("/movie", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie_endpoint(movie: MovieCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Creating movie: %s", movie.title)
        result = create_movie(movie, db)
        logger.info("Created movie with ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to create movie: %s, error: %s",
                     movie.title, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error creating movie: %s, error: %s", movie.title, str(e))
        raise


@router.put("/movie/{movie_id}", response_model=MovieResponse)
async def update_movie_endpoint(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Updating movie ID: %s", movie_id)
        result = update_movie(movie_id, movie, db)
        logger.info("Updated movie ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to update movie ID: %s, error: %s",
                     movie_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error updating movie ID: %s, error: %s", movie_id, str(e))
        raise


@router.patch("/movie/{movie_id}", response_model=MovieResponse)
async def partial_update_movie_endpoint(
    movie_id: int,
    title: Optional[str] = None,
    genre_id: Optional[int] = None,
    duration: Optional[int] = None,
    release_date: Optional[str] = None,
    description: Optional[str] = None,
    poster_url: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        logger.info("Partially updating movie ID: %s with title: %s, genre_id: %s",
                    movie_id, title, genre_id)
        result = partial_update_movie(
            movie_id, title, genre_id, duration, release_date, description, poster_url, db)
        logger.info("Partially updated movie ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error(
            "Failed to partially update movie ID: %s, error: %s", movie_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error partially updating movie ID: %s, error: %s", movie_id, str(e))
        raise


@router.delete("/movie/{movie_id}", response_model=dict)
async def delete_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Deleting movie ID: %s", movie_id)
        delete_movie(movie_id, db)
        logger.info("Deleted movie ID: %s", movie_id)
        return {"message": f"Movie {movie_id} deleted successfully"}
    except HTTPException as e:
        logger.error("Failed to delete movie ID: %s, error: %s",
                     movie_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error deleting movie ID: %s, error: %s", movie_id, str(e))
        raise


@router.post("/showtime", response_model=ShowtimeResponse, status_code=status.HTTP_201_CREATED)
async def create_showtime_endpoint(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Creating showtime for movie ID: %s, hall ID: %s",
                    showtime.movie_id, showtime.hall_id)
        result = create_showtime(showtime, db)
        logger.info("Created showtime with ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to create showtime for movie ID: %s, hall ID: %s, error: %s",
                     showtime.movie_id, showtime.hall_id, str(e.detail))
        raise
    except Exception as e:
        logger.error("Unexpected error creating showtime for movie ID: %s, hall ID: %s, error: %s",
                     showtime.movie_id, showtime.hall_id, str(e))
        raise


@router.put("/showtime/{showtime_id}", response_model=ShowtimeResponse)
async def update_showtime_endpoint(showtime_id: int, showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Updating showtime ID: %s", showtime_id)
        result = update_showtime(showtime_id, showtime, db)
        logger.info("Updated showtime ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to update showtime ID: %s, error: %s",
                     showtime_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error updating showtime ID: %s, error: %s", showtime_id, str(e))
        raise


@router.patch("/showtime/{showtime_id}", response_model=ShowtimeResponse)
async def partial_update_showtime_endpoint(
    showtime_id: int,
    movie_id: Optional[int] = None,
    hall_id: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    try:
        logger.info("Partially updating showtime ID: %s with movie_id: %s, hall_id: %s",
                    showtime_id, movie_id, hall_id)
        result = partial_update_showtime(
            showtime_id, movie_id, hall_id, start_time, end_time, price, db)
        logger.info("Partially updated showtime ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to partially update showtime ID: %s, error: %s",
                     showtime_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error partially updating showtime ID: %s, error: %s", showtime_id, str(e))
        raise


@router.delete("/showtime/{showtime_id}", response_model=dict)
async def delete_showtime_endpoint(showtime_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Deleting showtime ID: %s", showtime_id)
        delete_showtime(showtime_id, db)
        logger.info("Deleted showtime ID: %s", showtime_id)
        return {"message": f"Showtime {showtime_id} deleted successfully"}
    except HTTPException as e:
        logger.error("Failed to delete showtime ID: %s, error: %s",
                     showtime_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error deleting showtime ID: %s, error: %s", showtime_id, str(e))
        raise


@router.get("/users", response_model=List[UserResponse])
async def get_users_with_reservations_endpoint(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching users with reservations")
        result = get_users_with_reservations(db)
        logger.info("Fetched %s users with reservations", len(result))
        return result
    except HTTPException as e:
        logger.error(
            "Failed to fetch users with reservations, error: %s", str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error fetching users with reservations, error: %s", str(e))
        raise


@router.get("/total_sales", response_model=dict)
async def get_total_sales_endpoint(
    db: Session = Depends(get_db),
    cinema_id: Optional[int] = Query(None, description="Filter by cinema ID"),
    showtime_id: Optional[int] = Query(
        None, description="Filter by showtime ID"),
    start_date: Optional[datetime] = Query(
        None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(
        None, description="Filter by end date")
):
    try:
        logger.info("Fetching total sales with filters: cinema_id=%s, showtime_id=%s, start_date=%s, end_date=%s",
                    cinema_id, showtime_id, start_date, end_date)
        result = get_total_sales(
            db, cinema_id, showtime_id, start_date, end_date)
        logger.info("Fetched total sales: %s", result["total_sales"])
        return result
    except HTTPException as e:
        logger.error("Failed to fetch total sales with filters: cinema_id=%s, showtime_id=%s, error: %s",
                     cinema_id, showtime_id, str(e.detail))
        raise
    except Exception as e:
        logger.error("Unexpected error fetching total sales with filters: cinema_id=%s, showtime_id=%s, error: %s",
                     cinema_id, showtime_id, str(e))
        raise


@router.post("/reservation/{reservation_id}/approve", response_model=ReservationResponse)
async def approve_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Approving reservation ID: %s", reservation_id)
        result = approve_reservation(reservation_id, db)
        logger.info("Approved reservation ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to approve reservation ID: %s, error: %s",
                     reservation_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error approving reservation ID: %s, error: %s", reservation_id, str(e))
        raise


@router.post("/reservation/{reservation_id}/reject", response_model=ReservationResponse)
async def reject_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Rejecting reservation ID: %s", reservation_id)
        result = reject_reservation(reservation_id, db)
        logger.info("Rejected reservation ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to reject reservation ID: %s, error: %s",
                     reservation_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error rejecting reservation ID: %s, error: %s", reservation_id, str(e))
        raise
