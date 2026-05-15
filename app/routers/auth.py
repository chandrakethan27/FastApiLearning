"""
Auth router — /auth/register, /auth/login
Notice how SMALL this file is — all logic is in services/auth.py
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db, create_access_token
from app.schemas.user import UserRegister, UserResponse, TokenResponse
from app.services.auth import register_user, authenticate_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],    # groups these routes in /docs
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check if username is taken
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    return register_user(db, user.username, user.password)


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
