import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.features.users.models import User
from src.features.auth.services import get_current_user
from .services import create_reservation, cancel_reservation, get_available_seats, get_user_reservations
from .schemas import ReservationCreate, ReservationResponse, ReservationCancelResponse

router = APIRouter(tags=["reservation"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation_endpoint(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info("Creating reservation for user ID: %s, showtime ID: %s",
                current_user.id, reservation.showtime_id)
    result = create_reservation(reservation, current_user, db)
    logger.info("Created reservation with ID: %s", result.id)
    return result


@router.delete("/{reservation_id}", response_model=ReservationCancelResponse)
async def cancel_reservation_endpoint(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info("Cancelling reservation ID: %s by user ID: %s",
                reservation_id, current_user.id)
    result = cancel_reservation(reservation_id, current_user, db)
    logger.info("Cancelled reservation ID: %s", reservation_id)
    return result


@router.get("/showtime/{showtime_id}/seats")
async def get_available_seats_endpoint(showtime_id: int, db: Session = Depends(get_db)):
    logger.info("Fetching available seats for showtime ID: %s", showtime_id)
    result = get_available_seats(showtime_id, db)
    logger.info("Fetched %s available seats for showtime ID: %s",
                len(result["available_seats"]), showtime_id)
    return result


@router.get("/", response_model=list[ReservationResponse])
async def get_user_reservations_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info("Fetching reservations for user ID: %s", current_user.id)
    result = get_user_reservations(current_user, db)
    logger.info("Fetched %s reservations for user ID: %s",
                len(result), current_user.id)
    return result
