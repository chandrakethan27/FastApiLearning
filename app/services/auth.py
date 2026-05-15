"""
Auth business logic — separated from HTTP handling.
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import hash_password, verify_password


def register_user(db: Session, username: str, password: str) -> User:
    user = User(
        username=username,
        hashed_password=hash_password(password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
