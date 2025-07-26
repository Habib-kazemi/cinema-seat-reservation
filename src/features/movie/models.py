from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    duration = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(Text)
    poster_url = Column(String(255))
    showtime = relationship("Showtime", back_populates="movie")
    genre = relationship("Genre", back_populates="movies",
                         foreign_keys=[genre_id])
