from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from src.features.users.models import User
from src.features.users.schemas import UserCreate, Role
from src.config.settings import settings
from src.database import get_db
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError as exc:
        raise credentials_exception from exc


def register_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role if user.role else Role.USER,
        full_name=user.full_name,
        phone_number=user.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": f"User with id {db_user.id} created successfully"}


def login_user(form_data: OAuth2PasswordRequestForm, db: Session):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
