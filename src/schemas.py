"""
Pydantic schemas for API request/response validation
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for creating a new user
    """
    email: str
    password: str
    full_name: str
    phone_number: Optional[str] = None


class UserResponse(BaseModel):
    """
    Schema for user creation/retrieval response
    """
    id: int
    message: str


class MovieCreate(BaseModel):
    """
    Schema for creating a new movie
    """
    title: str
    genre_id: int
    duration: int
    release_date: date
    description: Optional[str] = None
    poster_url: Optional[str] = None


class MovieResponse(BaseModel):
    """
    Schema for movie creation response
    """
    id: int
    message: str


class ReservationCreate(BaseModel):
    """
    Schema for creating a new reservation
    """
    user_id: int
    showtime_id: int
    seat_number: str


class ReservationResponse(BaseModel):
    """
    Schema for reservation creation response
    """
    id: int
    message: str


class ShowtimeCreate(BaseModel):
    """
    Schema for creating a new showtime
    """
    movie_id: int
    hall_id: int
    start_time: datetime
    end_time: datetime
    price: float


class ShowtimeResponse(BaseModel):
    """
    Schema for showtime creation response
    """
    id: int
    message: str


class HallCreate(BaseModel):
    """
    Schema for creating a new hall
    """
    name: str
    rows: int
    columns: int


class HallResponse(BaseModel):
    """
    Schema for hall creation response
    """
    id: int
    message: str
