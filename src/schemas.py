"""
Pydantic schemas for API request and response validation.
"""
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


class Status(str, Enum):
    """Enum for reservation status."""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"


class BaseSchema(BaseModel):
    """Base schema with common configuration for all models."""
    model_config = ConfigDict(from_attributes=True)


class CinemaBase(BaseModel):
    """Base schema for cinema data."""
    name: str
    address: str


class CinemaCreate(CinemaBase):
    """Schema for creating a cinema."""


class CinemaResponse(CinemaBase, BaseSchema):
    """Schema for cinema response."""
    id: int
    halls: List["HallResponse"] = []  # Include related hall


class GenreBase(BaseModel):
    """Base schema for genre data."""
    name: str


class GenreCreate(GenreBase):
    """Schema for creating a genre."""


class GenreResponse(GenreBase, BaseSchema):
    """Schema for genre response."""
    id: int


class MovieBase(BaseModel):
    """Base schema for movie data."""
    title: str
    genre_id: int
    duration: int
    release_date: date
    description: Optional[str] = None
    poster_url: Optional[str] = None


class MovieBaseSimple(BaseModel):
    """Simplified schema for movie data in showtime."""
    id: int
    title: str


class MovieCreate(MovieBase):
    """Schema for creating a movie."""


class MovieResponse(MovieBase, BaseSchema):
    """Schema for movie response."""
    id: int


class HallBase(BaseModel):
    """Base schema for hall data."""
    name: str
    rows: int
    columns: int
    cinema_id: int  # Added to associate hall with cinema


class HallCreate(HallBase):
    """Schema for creating a hall."""


class HallResponse(HallBase, BaseSchema):
    """Schema for hall response."""
    id: int
    showtimes: List["ShowtimeResponse"] = []  # Updated to include showtime


class ShowtimeBase(BaseModel):
    """Base schema for showtime data."""
    movie_id: int
    hall_id: int
    start_time: datetime
    end_time: datetime
    price: float


class ShowtimeCreate(ShowtimeBase):
    """Schema for creating a showtime."""


class ShowtimeResponse(ShowtimeBase, BaseSchema):
    """Schema for showtime response."""
    id: int
    movie: MovieBaseSimple


class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str
    role: Optional[str] = "USER"  # Added role with default "USER"


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(UserBase, BaseSchema):
    """Schema for user response."""
    id: int
    role: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str


class ReservationBase(BaseModel):
    """Base schema for reservation data."""
    showtime_id: int
    seat_number: str


class ReservationCreate(ReservationBase):
    """Schema for creating a reservation."""


class ReservationResponse(ReservationBase, BaseSchema):
    """Schema for reservation response."""
    id: int
    user_id: int
    price: float
    created_at: datetime
    status: Status


class ReservationCancelResponse(BaseSchema):
    """Schema for reservation cancellation response."""
    message: str


class ReservationStatusUpdate(BaseSchema):
    """Schema for updating reservation status (approve/reject)."""
    status: Status
