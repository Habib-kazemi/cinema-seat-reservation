from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.features.showtime.models import Showtime
from src.features.hall.models import Hall
from src.features.users.models import User
from .models import Reservation, Status
from .schemas import ReservationCreate, ReservationResponse


def create_reservation(reservation: ReservationCreate, current_user: User, db: Session):
    showtime = db.query(Showtime).filter(
        Showtime.id == reservation.showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    existing_reservation = db.query(Reservation).filter(
        Reservation.showtime_id == reservation.showtime_id,
        Reservation.seat_number == reservation.seat_number,
    ).first()
    if existing_reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Seat already reserved")
    hall = db.query(Hall).filter(Hall.id == showtime.hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")
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
        status=Status.PENDING
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def cancel_reservation(reservation_id: int, current_user: User, db: Session):
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


def get_available_seats(showtime_id: int, db: Session):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    hall = db.query(Hall).filter(Hall.id == showtime.hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")
    reserved_seats = db.query(Reservation).filter(
        Reservation.showtime_id == showtime_id).all()
    reserved_seats = {seat.seat_number for seat in reserved_seats}
    available_seats = []
    for row in range(1, hall.rows + 1):
        row_letter = chr(ord('A') + row - 1)
        for col in range(1, hall.columns + 1):
            seat_number = f"{row_letter}{col}"
            if seat_number not in reserved_seats:
                available_seats.append(seat_number)
    return {"showtime_id": showtime_id, "available_seats": available_seats}


def get_user_reservations(current_user: User, db: Session) -> List[ReservationResponse]:
    reservations = db.query(Reservation).filter(
        Reservation.user_id == current_user.id).all()
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No reservation found")
    return reservations
