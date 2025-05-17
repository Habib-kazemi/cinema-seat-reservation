"""
User-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    try:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            email=user.email,
            password_hash=hashed_password,
            role="user",
            full_name=user.full_name,
            phone_number=user.phone_number
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"id": db_user.id, "message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": db_user.id, "message": f"User {db_user.full_name} retrieved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
