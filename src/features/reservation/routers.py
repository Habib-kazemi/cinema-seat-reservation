from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.features.users.models import User
from src.utils.check_admin import check_admin
from src.features.auth.services import get_current_user
from .services import create_reservation, cancel_reservation, get_available_seats, get_user_reservations, approve_reservation, reject_reservation
from .schemas import ReservationCreate, ReservationResponse, ReservationCancelResponse

router = APIRouter(tags=["reservation"])


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation_endpoint(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_reservation(reservation, current_user, db)


@router.delete("/{reservation_id}", response_model=ReservationCancelResponse)
async def cancel_reservation_endpoint(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cancel_reservation(reservation_id, current_user, db)


@router.get("/showtime/{showtime_id}/seats")
async def get_available_seats_endpoint(showtime_id: int, db: Session = Depends(get_db)):
    return get_available_seats(showtime_id, db)


@router.get("/", response_model=list[ReservationResponse])
async def get_user_reservations_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_reservations(current_user, db)


@router.post("/{reservation_id}/approve", response_model=ReservationResponse)
async def approve_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    return approve_reservation(reservation_id, db)


@router.post("/{reservation_id}/reject", response_model=ReservationResponse)
async def reject_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    return reject_reservation(reservation_id, db)
