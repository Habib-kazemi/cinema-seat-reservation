from datetime import date
from typing import Optional
from pydantic import BaseModel
from pydantic import field_serializer


class MovieBase(BaseModel):
    title: str
    genre_id: int
    duration: int
    release_date: date
    description: Optional[str] = None
    poster_url: Optional[str] = None


class MovieBaseSimple(BaseModel):
    id: int
    title: str


class MovieCreate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes = True

    @field_serializer('release_date')
    def serialize_date(self, dt: date) -> str:
        return dt.isoformat()
