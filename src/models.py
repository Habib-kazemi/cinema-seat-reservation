"""
Database models using SQLAlchemy
"""
import enum
from sqlalchemy import Column, Integer, String, Date, Text, Float, DateTime, Enum
from sqlalchemy.sql.functions import now
from .database import Base


class Role(str, enum.Enum):
    """
    Enum for user roles
    """
    ADMIN = "ADMIN"
    USER = "USER"


class Status(str, enum.Enum):
    """
    Enum for reservation statuses
    """
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"


class Genre(Base):
    """
    Model for movie genres
    """
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


class Movie(Base):
    """
    Model for movies
    """
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genre_id = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(Text)
    poster_url = Column(String(255))


class Hall(Base):
    """
    Model for cinema halls
    """
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)


class Showtime(Base):
    """
    Model for showtimes
    """
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, nullable=False)
    hall_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)


class User(Base):
    """
    Model for users
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(Role), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    created_at = Column(DateTime, server_default=now())


class Reservation(Base):
    """
    Model for reservations
    """
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    showtime_id = Column(Integer, nullable=False)
    seat_number = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(Enum(Status), nullable=False)
    created_at = Column(DateTime, server_default=now())
