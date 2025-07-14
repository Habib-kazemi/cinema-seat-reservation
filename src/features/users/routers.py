from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from .services import register_user, login_user
from .schemas import UserCreate, UserLogin, UserResponse
from src.features.auth.schemas import Token

router = APIRouter(tags=["users"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user.email, user.password, db)
