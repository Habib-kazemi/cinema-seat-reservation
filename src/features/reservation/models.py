from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from src.database import Base
from .schemas import Status


class Reservation(Base):
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
