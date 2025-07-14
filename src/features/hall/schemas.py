from pydantic import BaseModel
from typing import List
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
