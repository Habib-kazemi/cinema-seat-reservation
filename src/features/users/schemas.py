from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: Optional[str] = "USER"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
