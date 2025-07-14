from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class Cinema(Base):
    __tablename__ = "cinema"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    hall = relationship("Hall", back_populates="cinema")
