import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.features.user.models import User
from src.features.auth.services import get_current_user
from .services import create_reservation, cancel_reservation, get_available_seats, get_user_reservations
from .schemas import ReservationCreate, ReservationResponse, ReservationCancelResponse, SeatStatusResponse

router = APIRouter(tags=["reservation"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation_endpoint(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info("Creating reservation for user ID: %s, showtime ID: %s",
                    current_user.id, reservation.showtime_id)
        result = create_reservation(reservation, current_user, db)
        logger.info("Created reservation with ID: %s", result.id)
        return result
    except HTTPException as e:
        logger.error("Failed to create reservation for user ID: %s, showtime ID: %s, error: %s",
                     current_user.id, reservation.showtime_id, str(e.detail))
        raise
    except Exception as e:
        logger.error("Unexpected error creating reservation for user ID: %s, showtime ID: %s, error: %s",
                     current_user.id, reservation.showtime_id, str(e))
        raise


@router.delete("/{reservation_id}", response_model=ReservationCancelResponse)
async def cancel_reservation_endpoint(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info("Cancelling reservation ID: %s by user ID: %s",
                    reservation_id, current_user.id)
        result = cancel_reservation(reservation_id, current_user, db)
        logger.info("Cancelled reservation ID: %s", reservation_id)
        return result
    except HTTPException as e:
        logger.error("Failed to cancel reservation ID: %s by user ID: %s, error: %s",
                     reservation_id, current_user.id, str(e.detail))
        raise
    except Exception as e:
        logger.error("Unexpected error cancelling reservation ID: %s by user ID: %s, error: %s",
                     reservation_id, current_user.id, str(e))
        raise


@router.get("/showtime/{showtime_id}/seat", response_model=SeatStatusResponse)
async def get_available_seats_endpoint(showtime_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Fetching available seats for showtime ID: %s", showtime_id)
        result = get_available_seats(showtime_id, db)
        logger.info("Fetched %s seats for showtime ID: %s",
                    len(result["available_seat"]), showtime_id)
        return result
    except HTTPException as e:
        logger.error("Failed to fetch available seats for showtime ID: %s, error: %s",
                     showtime_id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error fetching available seats for showtime ID: %s, error: %s", showtime_id, str(e))
        raise


@router.get("/", response_model=list[ReservationResponse])
async def get_user_reservations_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.info("Fetching reservations for user ID: %s", current_user.id)
        result = get_user_reservations(current_user, db)
        logger.info("Fetched %s reservations for user ID: %s",
                    len(result), current_user.id)
        return result
    except HTTPException as e:
        logger.error("Failed to fetch reservations for user ID: %s, error: %s",
                     current_user.id, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error fetching reservations for user ID: %s, error: %s", current_user.id, str(e))
        raise
