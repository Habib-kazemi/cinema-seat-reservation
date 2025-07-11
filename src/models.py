"""
Database models using SQLAlchemy
"""
import enum
from sqlalchemy import Column, Integer, String, Date, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship
from .database import Base


class Role(str, enum.Enum):
    """
    Enum for user roles
    """
    ADMIN = "ADMIN"
    USER = "USER"


class Status(str, enum.Enum):
    """
    Enum for reservation status
    """
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"


class Cinema(Base):  # pylint: disable=too-few-public-methods
    """
    Model for cinema
    """
    __tablename__ = "cinema"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    # Relationship with Hall
    hall = relationship("Hall", back_populates="cinema")


class Genre(Base):  # pylint: disable=too-few-public-methods
    """
    Model for movie genre
    """
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


class Movie(Base):  # pylint: disable=too-few-public-methods
    """
    Model for movie
    """
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    duration = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(Text)
    poster_url = Column(String(255))
    showtime = relationship("Showtime", back_populates="movie")


class Hall(Base):  # pylint: disable=too-few-public-methods
    """
    Model for cinema hall
    """
    __tablename__ = "hall"
    id = Column(Integer, primary_key=True, index=True)
    cinema_id = Column(Integer, ForeignKey("cinema.id"), nullable=False)
    name = Column(String(100), nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    # Added relationship
    cinema = relationship("Cinema", back_populates="hall")
    showtime = relationship("Showtime", back_populates="hall")


class Showtime(Base):  # pylint: disable=too-few-public-methods
    """
    Model for showtime
    """
    __tablename__ = "showtime"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("hall.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    movie = relationship("Movie", back_populates="showtime")
    hall = relationship("Hall", back_populates="showtime")
    reservation = relationship("Reservation", back_populates="showtime")


class User(Base):  # pylint: disable=too-few-public-methods
    """
    Model for users
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    created_at = Column(DateTime, server_default=now())
    reservation = relationship(
        "Reservation", back_populates="user", cascade="all, delete-orphan")


class Reservation(Base):  # pylint: disable=too-few-public-methods
    """
    Model for reservation
    """
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    showtime_id = Column(Integer, ForeignKey("showtime.id"), nullable=False)
    seat_number = Column(String(10), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=now())
    user = relationship("User", back_populates="reservation")
    showtime = relationship("Showtime", back_populates="reservation")
