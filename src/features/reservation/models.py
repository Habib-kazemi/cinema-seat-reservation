from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from src.database import Base
from .schemas import Status
from src.features.user.models import User


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    showtime_id = Column(Integer, ForeignKey("showtime.id"), nullable=False)
    position_id = Column(Integer, ForeignKey(
        "hall_position.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.PENDING)
    created_at = Column(DateTime, server_default=now())
    user = relationship("User", back_populates="reservation")
    showtime = relationship("Showtime", back_populates="reservation")
    position = relationship("Hall_position")
