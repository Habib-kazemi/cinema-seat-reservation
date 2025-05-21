"""
Reservation-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Reservation, User, Showtime, Status
from ..schemas import ReservationCreate, ReservationResponse

router = APIRouter()


@router.post("/", response_model=ReservationResponse)
async def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    """
    Create a new seat reservation for a showtime.

    Args:
        reservation: Reservation data including user_id, showtime_id, and seat_number.
        db: Database session.

    Returns:
        dict: Reservation ID and success message.

    Raises:
        HTTPException: If user, showtime, or seat is invalid or already reserved.
    """
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == reservation.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if showtime exists
        showtime = db.query(Showtime).filter(
            Showtime.id == reservation.showtime_id).first()
        if not showtime:
            raise HTTPException(status_code=404, detail="Showtime not found")

        # Check if seat is already reserved
        existing_reservation = db.query(Reservation).filter(
            Reservation.showtime_id == reservation.showtime_id,
            Reservation.seat_number == reservation.seat_number
        ).first()
        if existing_reservation:
            raise HTTPException(
                status_code=400, detail="Seat already reserved")

        # Create new reservation
        db_reservation = Reservation(
            user_id=reservation.user_id,
            showtime_id=reservation.showtime_id,
            seat_number=reservation.seat_number,
            price=showtime.price,
            status=Status.PENDING
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)

        return {"id": db_reservation.id, "message": "Reservation created successfully"}

    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        print(f"Error in create_reservation: {exc}")
        raise HTTPException(
            status_code=500, detail="Internal server error") from exc
