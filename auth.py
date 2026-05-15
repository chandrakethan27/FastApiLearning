from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

# --- Config (hardcoded for learning — use env vars in production!) ---
SECRET_KEY = "super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
EXPIRY_MINUTES = 30

# --- Password hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# --- JWT token creation ---
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- JWT token decoding ---
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# --- Schemas ---
class UserRegister(BaseModel):
    username: str
    password: str


class UserProfile(BaseModel):
    username: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Fake user database ---
# In real apps, this would be a real database (like Lesson 5)
users_db: dict[str, dict] = {}


# --- OAuth2 scheme — tells FastAPI where the login endpoint is ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- The auth dependency — use this to protect any route ---
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    This dependency:
    1. Extracts the Bearer token from the Authorization header
    2. Decodes the JWT
    3. Finds the user in the database
    4. Returns the user (or raises 401)
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return users_db[username]
