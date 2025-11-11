# tests/test_user.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.schemas.base import UserCreate
from app.operations.user import create_user, get_user_by_username


# ---------------------------------------------------------------------
# TEST DATABASE SETUP
# ---------------------------------------------------------------------
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    """Creates a fresh test database schema for all tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------------------
# UNIT TESTS
# ---------------------------------------------------------------------

def test_password_hash_and_verify():
    """Ensure password hashing and verification works properly."""
    pw = "Secure123"
    hashed = User.hash_password(pw)
    assert hashed != pw  # should not be stored as plaintext
    assert User().verify_password(pw) is False  # random user should not verify
    # Create user with same hash manually
    u = User(password_hash=hashed)
    assert u.verify_password(pw) is True


def test_usercreate_schema_validation():
    """Ensure UserCreate schema validates proper data."""
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "username": "alicesmith",
        "password": "StrongPass1"
    }
    user = UserCreate(**data)
    assert user.username == "alicesmith"
    assert user.email == "alice@example.com"


def test_usercreate_password_strength():
    """Ensure weak passwords raise validation errors."""
    bad_pw_data = {
        "first_name": "Bob",
        "last_name": "Weak",
        "email": "bob@example.com",
        "username": "bobweak",
        "password": "weakpass"  # no uppercase or digit
    }
    with pytest.raises(ValueError):
        UserCreate(**bad_pw_data)


# ---------------------------------------------------------------------
# INTEGRATION TESTS (Postgres)
# ---------------------------------------------------------------------

def test_create_and_retrieve_user(db):
    """Create a user and ensure retrieval works."""
    user_data = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        username="johndoe",
        password="Secure123"
    )
    created = create_user(db, user_data)
    fetched = get_user_by_username(db, "johndoe")
    assert fetched.email == created.email
    assert fetched.username == "johndoe"
    assert fetched.is_active is True


def test_duplicate_user_raises(db):
    """Ensure duplicate email or username raises ValueError."""
    user_data = UserCreate(
        first_name="Jane",
        last_name="Doe",
        email="john@example.com",  # duplicate email
        username="janedoe",
        password="Secure123"
    )
    with pytest.raises(ValueError):
        create_user(db, user_data)


def test_invalid_email_format():
    bad_email_data = {
        "first_name": "Invalid",
        "last_name": "Email",
        "email": "not-an-email",
        "username": "invaliduser",
        "password": "StrongPass123"
    }
    import pytest
    from app.schemas.base import UserCreate
    with pytest.raises(ValueError):
        UserCreate(**bad_email_data)

def test_username_case_insensitivity(db):
    data1 = {"first_name": "A", "last_name": "B", "email": "a@b.com", "username": "TestUser", "password": "Strong123"}
    data2 = {"first_name": "C", "last_name": "D", "email": "c@d.com", "username": "testuser", "password": "Strong123"}
    create_user(db, UserCreate(**data1))
    with pytest.raises(ValueError):
        create_user(db, UserCreate(**data2))

def test_missing_required_field():
    incomplete = {"first_name": "John", "last_name": "Doe", "password": "Strong123"}
    from app.schemas.base import UserCreate
    import pytest
    with pytest.raises(ValueError):
        UserCreate(**incomplete)
