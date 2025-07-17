from datetime import datetime
from pydantic import BaseModel, field_validator, field_serializer
from src.features.movie.schemas import MovieResponse


class ShowtimeBase(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime
    end_time: datetime
    price: float


class ShowtimeCreate(ShowtimeBase):
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, end_time: datetime, values) -> datetime:
        start_time = values.data.get('start_time')
        if start_time and end_time <= start_time:
            raise ValueError('End time must be after start time')
        return end_time


class ShowtimeResponse(ShowtimeBase):
    id: int
    movie: MovieResponse

    class Config:
        from_attributes = True

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat()
