# app/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.operations.user import create_user, get_user_by_username
from app.schemas.base import UserCreate
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:    # pragma: no cover
        return create_user(db, user)    
    except ValueError as e: # pragma: no cover
        raise HTTPException(status_code=400, detail=str(e)) 

@router.get("/{username}", response_model=UserRead)
def read_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # pragma: no cover
    return user # pragma: no cover
