# tests/integration/test_database.py
from sqlalchemy import inspect
from app.database import engine, Base
from app.database_init import init_db

def test_users_table_exists():
    # Ensure tables are created before inspecting
    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables

def test_init_db_creates_tables():
    init_db()
    inspector = inspect(engine)
    assert "users" in inspector.get_table_names()
