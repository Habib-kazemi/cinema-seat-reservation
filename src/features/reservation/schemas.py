from datetime import datetime
from enum import Enum
from pydantic import BaseModel, field_serializer
from typing import List


class Status(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"


class SeatStatus(BaseModel):
    position_id: int
    row_index: int
    column_index: int
    status: str


class SeatStatusResponse(BaseModel):
    showtime_id: int
    available_seat: List[SeatStatus]


class ReservationBase(BaseModel):
    showtime_id: int
    row_index: int
    column_index: int


class ReservationCreate(ReservationBase):
    pass


class ReservationResponse(ReservationBase):
    id: int
    user_id: int
    position_id: int
    price: float
    created_at: datetime
    status: Status

    class Config:
        from_attributes = True

    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat()


class ReservationCancelResponse(BaseModel):
    message: str


class ReservationStatusUpdate(BaseModel):
    status: Status
