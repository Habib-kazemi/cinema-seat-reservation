"""API routes for managing seat reservations."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import Reservation, Showtime, User
from ..schemas import ReservationCreate, ReservationResponse

router = APIRouter()


@router.post("/", response_model=ReservationResponse)
async def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReservationResponse:
    """Create a new seat reservation for a showtime.

    Args:
        reservation: Reservation data (user_id, showtime_id, seat_number).
        db: Database session.
        current_user: Authenticated user.

    Returns:
        Reservation ID and success message.

    Raises:
        HTTPException: If user, showtime, or seat is invalid, or if unauthorized.
    """
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = db.query(User).filter(User.id == reservation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    showtime = db.query(Showtime).filter(
        Showtime.id == reservation.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    existing_reservation = db.query(Reservation).filter(
        Reservation.showtime_id == reservation.showtime_id,
        Reservation.seat_number == reservation.seat_number,
    ).first()
    if existing_reservation:
        raise HTTPException(status_code=400, detail="Seat already reserved")
    if not isinstance(showtime.price, (int, float, Decimal)):
        raise HTTPException(status_code=500, detail="Invalid price format")
    db_reservation = Reservation(
        user_id=reservation.user_id,
        showtime_id=reservation.showtime_id,
        seat_number=reservation.seat_number,
        price=float(showtime.price),
        status="pending",
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return {"id": db_reservation.id, "message": "Reservation created successfully"}
