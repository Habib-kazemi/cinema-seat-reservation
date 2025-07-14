from datetime import datetime
from typing import Dict
from pydantic import BaseModel
from pydantic import field_serializer


class ShowtimeBase(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime
    end_time: datetime
    price: float


class ShowtimeCreate(ShowtimeBase):
    pass


class ShowtimeResponse(ShowtimeBase):
    id: int
    movie: Dict

    class Config:
        from_attributes = True

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat()
