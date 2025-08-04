from typing import List
from pydantic import BaseModel
from src.features.showtime.schemas import ShowtimeResponse


class HallBase(BaseModel):
    name: str
    rows: int
    columns: int
    cinema_id: int


class HallCreate(HallBase):
    pass


class HallResponse(HallBase):
    id: int
    showtimes: List[ShowtimeResponse] = []

    class Config:
        from_attributes = True
