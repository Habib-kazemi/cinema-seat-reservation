from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.features.showtime.models import Showtime
from src.features.hall.models import Hall, Hall_position
from src.features.users.models import User
from .models import Reservation, Status
from .schemas import ReservationCreate, ReservationResponse


def create_reservation(reservation: ReservationCreate, current_user: User, db: Session):
    showtime = db.query(Showtime).filter(
        Showtime.id == reservation.showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    position = db.query(Hall_position).filter(
        Hall_position.hall_id == showtime.hall_id,
        Hall_position.row_index == reservation.row_index,
        Hall_position.column_index == reservation.column_index
    ).first()
    if not position:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid seat position")
    if reservation.row_index < 1 or reservation.row_index > showtime.hall.rows or reservation.column_index < 1 or reservation.column_index > showtime.hall.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid seat position")
    existing_reservation = db.query(Reservation).filter(
        Reservation.showtime_id == reservation.showtime_id,
        Reservation.position_id == position.id,
        Reservation.status != Status.CANCELED
    ).first()
    if existing_reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Seat already reserved")
    db_reservation = Reservation(
        user_id=current_user.id,
        showtime_id=reservation.showtime_id,
        position_id=position.id,
        price=reservation.price,
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
    reservation.status = Status.CANCELED
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
    reserved_positions = db.query(Reservation.position_id).filter(
        Reservation.showtime_id == showtime_id,
        Reservation.status != Status.CANCELED
    ).all()
    reserved_position_ids = [pos_id for (pos_id,) in reserved_positions]
    available_positions = db.query(Hall_position).filter(
        Hall_position.hall_id == showtime.hall_id,
        ~Hall_position.id.in_(reserved_position_ids)
    ).all()
    return {
        "showtime_id": showtime_id,
        "available_seats": [
            {"row_index": pos.row_index, "column_index": pos.column_index}
            for pos in available_positions
        ]
    }


def get_user_reservations(current_user: User, db: Session) -> List[ReservationResponse]:
    reservations = db.query(Reservation).filter(
        Reservation.user_id == current_user.id).all()
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No reservation found")
    return reservations
