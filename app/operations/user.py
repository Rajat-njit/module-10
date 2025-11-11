# app/operations/user.py
from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserRead
from app.schemas.base import UserCreate

def create_user(db: Session, data: UserCreate) -> UserRead:
    new_user = User.register(db, data.model_dump())
    db.commit()
    db.refresh(new_user)
    return UserRead.model_validate(new_user)

def get_user_by_username(db: Session, username: str) -> Optional[UserRead]:
    user = db.query(User).filter(User.username == username).first()
    return UserRead.model_validate(user) if user else None
