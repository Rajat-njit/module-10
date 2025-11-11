# app/models/user.py
from datetime import datetime
import uuid
from typing import Dict, Any, Optional

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates


from passlib.context import CryptContext
from app.database import Base
from app.schemas.base import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # -------------------------------------------------------------------
    # Password helpers
    # -------------------------------------------------------------------
    @staticmethod
        def hash_password(password: str) -> str:
            """
            Securely hash the user's password.
            bcrypt only supports up to 72 bytes, so longer inputs are truncated safely.
            """
            if len(password.encode("utf-8")) > 72:
                password = password[:72]  # truncate safely for bcrypt
            return pwd_context.hash(password)


    def verify_password(self, plain_password: str) -> bool:
        """Return True if the plain password matches stored hash."""
        return pwd_context.verify(plain_password, self.password_hash)

    # -------------------------------------------------------------------
    # Registration helper
    # -------------------------------------------------------------------
    @classmethod
    def register(cls, db, user_data: Dict[str, Any]) -> "User":
        """Create and return a validated, hashed User object."""
        validated = UserCreate.model_validate(user_data)

        # Check for duplicates
        existing = db.query(cls).filter(
            (cls.email == validated.email) | (cls.username == validated.username)
        ).first()
        if existing:
            raise ValueError("Username or email already exists.")

        new_user = cls(
            first_name=validated.first_name,
            last_name=validated.last_name,
            email=validated.email,
            username=validated.username,
            password_hash=cls.hash_password(validated.password),
        )
        db.add(new_user)
        db.flush()       # assign id without full commit
        return new_user

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
