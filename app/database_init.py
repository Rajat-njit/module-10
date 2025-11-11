# app/database_init.py
from app.database import Base, engine
from app.models import User

def init_db():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)

def drop_db():
    print("Dropping all tables...") # pragma: no cover
    Base.metadata.drop_all(bind=engine) # pragma: no cover
