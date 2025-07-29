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
    cinema = relationship("Cinema", back_populates="halls")
    positions = relationship("Hall_position", back_populates="hall")


class Hall_position(Base):
    __tablename__ = "hall_position"
    id = Column(Integer, primary_key=True, index=True)
    hall_id = Column(Integer, ForeignKey("hall.id"), nullable=False)
    row_index = Column(Integer, nullable=False)
    column_index = Column(Integer, nullable=False)
    hall = relationship("Hall", back_populates="positions")
