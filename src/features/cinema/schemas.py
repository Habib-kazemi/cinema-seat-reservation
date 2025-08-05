from typing import List
from pydantic import BaseModel
from src.features.hall.schemas import HallResponse


class CinemaBase(BaseModel):
    name: str
    address: str


class CinemaCreate(CinemaBase):
    pass


class CinemaResponse(CinemaBase):
    id: int
    halls: List[HallResponse] = []

    class Config:
        from_attributes = True
