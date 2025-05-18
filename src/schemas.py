"""
Pydantic schemas for API request/response validation
"""
from datetime import date
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
