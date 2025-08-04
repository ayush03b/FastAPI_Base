from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps import get_db
from schemas import UserLogin, Token
from utils import verify_password
from models import User
from oath2 import create_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_credentials.email).first()
    if not db_user:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if not verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    access_token = create_access_token(data={"user_id": db_user.id})
    return Token(access_token=access_token, token_type="Bearer")
