from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from pydantic import field_serializer


class Status(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"


class ReservationBase(BaseModel):
    showtime_id: int
    seat_number: str


class ReservationCreate(ReservationBase):
    pass


class ReservationResponse(ReservationBase):
    id: int
    user_id: int
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
