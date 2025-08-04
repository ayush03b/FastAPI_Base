from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db
from schemas import UserResponse, UserCreate, UserUpdate, UserWithBooks
from models import User
from typing import List
from passlib.context import CryptContext
from utils import get_password_hash

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/users/{user_id}", response_model=UserWithBooks)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = (
        db.query(User)
        .filter((User.email == user.email) | (User.username == user.username))
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email or username already exists"
        )

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump(exclude_unset=True)

    # Check for unique constraints
    if "email" in update_data:
        existing_user = (
            db.query(User)
            .filter(User.email == update_data["email"], User.id != user_id)
            .first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

    if "username" in update_data:
        existing_user = (
            db.query(User)
            .filter(User.username == update_data["username"], User.id != user_id)
            .first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # TODO: only allow deletion if the user is the current user
    db.delete(user)
    db.commit()
    return None
