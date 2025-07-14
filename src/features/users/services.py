from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import User, Role
from .schemas import UserCreate, UserResponse
import bcrypt
from jose import jwt
from src.config.settings import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict) -> str:
    from datetime import datetime, timedelta, timezone
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire, "role": data.get("role", "USER")})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def register_user(user: UserCreate, db: Session) -> UserResponse:
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        role=Role.USER,
        full_name=user.full_name,
        phone_number=user.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(email: str, password: str, db: Session) -> dict:
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
