import logging
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.features.users.schemas import UserCreate
from .services import register_user, login_user
from .schemas import Token

router = APIRouter(tags=["auth"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering user: {user.email}")
    return register_user(user, db)


@router.post("/login", response_model=Token)
async def login_user_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: {form_data.username}")
    return login_user(form_data, db)
