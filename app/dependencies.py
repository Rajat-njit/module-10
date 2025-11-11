# app/dependencies.py
from app.database import SessionLocal

# Standard dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
