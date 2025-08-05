import logging
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.features.user.schemas import UserCreate
from .services import register_user, login_user
from .schemas import Token

router = APIRouter(tags=["auth"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Registering user: %s", user.email)
        result = register_user(user, db)
        logger.info("Registered user with ID: %s",
                    result["message"].split()[-2])
        return result
    except HTTPException as e:
        logger.error("Failed to register user: %s, error: %s",
                     user.email, str(e.detail))
        raise
    except Exception as e:
        logger.error(
            "Unexpected error registering user: %s, error: %s", user.email, str(e))
        raise


@router.post("/login", response_model=Token)
async def login_user_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        logger.info("Login attempt for user: %s", form_data.username)
        result = login_user(form_data, db)
        logger.info("User %s logged in successfully", form_data.username)
        return result
    except HTTPException as e:
        logger.error("Failed to login user: %s, error: %s",
                     form_data.username, str(e.detail))
        raise
    except Exception as e:
        logger.error("Unexpected error logging in user: %s, error: %s",
                     form_data.username, str(e))
        raise
