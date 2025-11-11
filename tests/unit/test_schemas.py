import pytest
from app.schemas.base import UserCreate
from pydantic import ValidationError

def test_valid_user_schema():
    user = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        username="johndoe",
        password="StrongPass1"
    )
    assert user.email == "john@example.com"

def test_invalid_email_schema():
    with pytest.raises(ValueError):
        UserCreate(
            first_name="John",
            last_name="Doe",
            email="invalid-email",
            username="user",
            password="StrongPass1"
        )

def test_invalid_email_raises_error():
    with pytest.raises(ValidationError):
        UserCreate(username="raj", email="invalid-email", password="StrongPass123")
