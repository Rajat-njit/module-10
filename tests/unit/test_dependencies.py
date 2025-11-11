from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.database import get_engine, SessionLocal

def test_get_db_returns_session():
    gen = get_db()
    db = next(gen)
    assert isinstance(db, Session)
    gen.close()

def test_get_engine_returns_engine_instance():
    engine = get_engine()
    assert "Engine" in str(type(engine))

def test_session_local_creates_session():
    session = SessionLocal()
    assert session is not None
    session.close()
