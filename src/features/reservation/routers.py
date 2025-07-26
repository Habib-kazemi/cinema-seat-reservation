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
    logger.info(
        f"Creating reservation for user ID: {current_user.id}, showtime ID: {reservation.showtime_id}")
    return create_reservation(reservation, current_user, db)


@router.delete("/{reservation_id}", response_model=ReservationCancelResponse)
async def cancel_reservation_endpoint(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(
        f"Cancelling reservation ID: {reservation_id} by user ID: {current_user.id}")
    return cancel_reservation(reservation_id, current_user, db)


@router.get("/showtime/{showtime_id}/seats")
async def get_available_seats_endpoint(showtime_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching available seats for showtime ID: {showtime_id}")
    return get_available_seats(showtime_id, db)


@router.get("/", response_model=list[ReservationResponse])
async def get_user_reservations_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"Fetching reservations for user ID: {current_user.id}")
    return get_user_reservations(current_user, db)
