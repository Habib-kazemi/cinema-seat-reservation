"""Pydantic schemas for API request and response validation."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseSchema(BaseModel):
    """Base schema with common configuration for all models."""
    model_config = ConfigDict(from_attributes=True)


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


class HallCreate(HallBase):
    """Schema for creating a hall."""


class HallResponse(HallBase, BaseSchema):
    """Schema for hall response."""
    id: int


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


class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


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
    user_id: int
    showtime_id: int
    seat_number: str


class ReservationCreate(ReservationBase):
    """Schema for creating a reservation."""


class ReservationResponse(BaseSchema):
    """Schema for reservation response."""
    id: int
    message: str


class ReservationCancelResponse(BaseSchema):
    """Schema for reservation cancellation response."""
    message: str
