# app/schemas/base.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

class UserBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    model_config = ConfigDict(from_attributes=True)

class PasswordMixin(BaseModel):
    password: str = Field(min_length=6, max_length=128)

    @model_validator(mode="before")
    @classmethod
    def check_strength(cls, values: dict):
        pw = values.get("password", "")
        if not any(c.isupper() for c in pw): 
            raise ValueError("Password must contain an uppercase letter")   # pragma: no cover
        if not any(c.islower() for c in pw):
            raise ValueError("Password must contain a lowercase letter")    # pragma: no cover
        if not any(c.isdigit() for c in pw):
            raise ValueError("Password must contain a number")  # pragma: no cover
        return values

class UserCreate(UserBase, PasswordMixin):
    """Schema used when creating a new user."""
    pass
