"""
Reservation-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import Hall, Reservation, Showtime, User, Status
from ..schemas import ReservationCreate, ReservationResponse, ReservationCancelResponse

router = APIRouter(tags=["reservation"])


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new reservation."""
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
        user_id=current_user.id,
        showtime_id=reservation.showtime_id,
        seat_number=reservation.seat_number,
        price=showtime.price,
        status=Status.PENDING  # Changed to PENDING instead of CONFIRMED
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


@router.get("/showtimes/{showtime_id}/seats")
async def get_available_seats(
    showtime_id: int,
    db: Session = Depends(get_db)
):
    """
    Get available seats for a showtime.

    Args:
        showtime_id: ID of the showtime.
        db: Database session.

    Returns:
        List of available seat numbers (e.g., ["A12", "B5"]).

    Raises:
        HTTPException: If showtime or hall is not found.
    """
    # Check if showtime exists
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")

    # Get hall details
    hall = db.query(Hall).filter(Hall.id == showtime.hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")

    # Get reserved seats for this showtime
    reserved_seats = db.query(Reservation).filter(
        Reservation.showtime_id == showtime_id).all()
    reserved_seats = {seat.seat_number for seat in reserved_seats}

    # Generate available seats
    available_seats = []
    for row in range(1, hall.rows + 1):
        row_letter = chr(ord('A') + row - 1)  # A, B, C, ...
        for col in range(1, hall.columns + 1):
            seat_number = f"{row_letter}{col}"
            if seat_number not in reserved_seats:
                available_seats.append(seat_number)

    return {"showtime_id": showtime_id, "available_seats": available_seats}


@router.get("/", response_model=list[ReservationResponse])
async def get_user_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all reservations for the current user.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        List of user's reservations.

    Raises:
        HTTPException: If no reservations are found.
    """
    reservation = db.query(Reservation).filter(
        Reservation.user_id == current_user.id).all()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No reservation found")
    return reservation
