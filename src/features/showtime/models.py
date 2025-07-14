from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from src.database import Base


class Showtime(Base):
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
