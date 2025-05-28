"""API routes for user authentication and management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import create_access_token, hash_password, verify_password
from ..database import get_db
from ..models import Role, User
from ..schemas import Token, UserCreate, UserLogin, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Register a new user.

    Args:
        user: User creation data.
        db: Database session.

    Returns:
        Created user details.

    Raises:
        HTTPException: If email is already registered.
    """
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


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Authenticate user and return JWT token.

    Args:
        user: User login credentials.
        db: Database session.

    Returns:
        JWT token and token type.

    Raises:
        HTTPException: If credentials are invalid.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
