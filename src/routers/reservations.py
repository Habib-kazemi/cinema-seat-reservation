"""
Reservation-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import Hall, Reservation, Showtime, User
from ..schemas import ReservationCreate, ReservationResponse, ReservationCancelResponse

router = APIRouter(tags=["reservations"])


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new reservation."""
    # Check if user_id matches current user
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cannot create reservation for another user")

    # Check if showtime exists
    showtime = db.query(Showtime).filter(
        Showtime.id == reservation.showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")

    # Check if seat is already reserved
    existing_reservation = db.query(Reservation).filter(
        Reservation.showtime_id == reservation.showtime_id,
        Reservation.seat_number == reservation.seat_number,
    ).first()
    if existing_reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Seat already reserved")

    # Validate seat number format and range
    hall = db.query(Hall).filter(Hall.id == showtime.hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")

    # Assume seat_number format is like "A12"
    try:
        row_letter = reservation.seat_number[0].upper()
        col_number = int(reservation.seat_number[1:])
        row_index = ord(row_letter) - ord('A') + 1
        if row_index < 1 or row_index > hall.rows or col_number < 1 or col_number > hall.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid seat number")
    except (ValueError, IndexError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid seat number format") from exc

    db_reservation = Reservation(
        user_id=reservation.user_id,
        showtime_id=reservation.showtime_id,
        seat_number=reservation.seat_number,
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


@router.delete("/{reservation_id}", response_model=ReservationCancelResponse)
async def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cancel a reservation."""
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to cancel this reservation")
    db.delete(reservation)
    db.commit()
    return {"message": "Reservation cancelled successfully"}
