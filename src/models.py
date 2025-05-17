"""
Database models using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Date, Text, Float, DateTime, Enum
from sqlalchemy.sql import func
from .database import Base
import enum


class Role(str, enum.Enum):
    admin = "admin"
    user = "user"


class Status(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genre_id = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(Text)
    poster_url = Column(String(255))


class Hall(Base):
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)


class Showtime(Base):
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, nullable=False)
    hall_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(Role), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    showtime_id = Column(Integer, nullable=False)
    seat_number = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(Enum(Status), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
