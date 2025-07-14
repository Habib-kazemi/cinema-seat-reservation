from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Hall(Base):
    __tablename__ = "hall"
    id = Column(Integer, primary_key=True, index=True)
    cinema_id = Column(Integer, ForeignKey("cinema.id"), nullable=False)
    name = Column(String(100), nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    cinema = relationship("Cinema", back_populates="hall")
    showtime = relationship("Showtime", back_populates="hall")
