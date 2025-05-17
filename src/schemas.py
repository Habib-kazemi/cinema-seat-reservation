"""
Pydantic schemas for API request/response validation
"""
from typing import Optional
from datetime import date
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    phone_number: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    message: str


class MovieCreate(BaseModel):
    title: str
    genre_id: int
    duration: int
    release_date: date
    description: Optional[str] = None
    poster_url: Optional[str] = None


class MovieResponse(BaseModel):
    id: int
    message: str
