
"""
Authentication routes for user registration and login.
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Dict
from dotenv import load_dotenv

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Role, User
from ..schemas import Token, UserCreate

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(tags=["auth"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password to hash.

    Returns:
        Hashed password as string.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash.

    Args:
        plain_password: Plain text password to verify.
        hashed_password: Hashed password to compare against.

    Returns:
        True if password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: Dict) -> str:
    """Create a JWT access token.

    Args:
        data: Dictionary containing token payload (e.g., user email).

    Returns:
        Encoded JWT token as string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Retrieve the authenticated user from JWT token.

    Args:
        token: JWT token from request header.
        db: Database session.

    Returns:
        User object if authenticated.

    Raises:
        HTTPException: If token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError as exc:
        raise credentials_exception from exc


@router.post("/register", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user: User data including email, password, and full_name.
        db: Database session.

    Returns:
        Dict with success message.

    Raises:
        HTTPException: If email already exists.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        role=Role.USER,
        full_name=user.full_name,
        phone_number=user.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": f"User with id {db_user.id} created successfully"}


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login a user and return JWT token.

    Args:
        form_data: OAuth2 form data with username (email) and password.
        db: Database session.

    Returns:
        Token object with access token.

    Raises:
        HTTPException: If credentials are invalid.
    """
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
