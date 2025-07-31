from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from passlib.context  import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")


# This is a dependency function that provides a SQLAlchemy session to any route that includes db: Session = Depends(get_db)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model = schemas.UserOut)

def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password =  pwd_context.hash(user.password)
    new_user = models.User(
        username = user.username,
        email= user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user