from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings

Base = declarative_base()

def get_engine(database_url: str = settings.DATABASE_URL):
    try:
        return create_engine(database_url, echo=True)
    except SQLAlchemyError as e:    # pragma: no cover
        print(f"Error creating engine: {e}")
        raise

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():   
    db = SessionLocal() # pragma: no cover
    try:    # pragma: no cover
        yield db    
    finally:
        db.close() # pragma: no cover
