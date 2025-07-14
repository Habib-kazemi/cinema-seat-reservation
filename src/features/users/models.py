from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship
from src.database import Base
from .schemas import Role


class User(Base):
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
