from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, database, auth
from app.database import get_db

from passlib.context import CryptContext

router = APIRouter(
    prefix = "/login",
    tags = ["login"]
)

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")
@router.post("/")

def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user= db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    access_token = auth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}