from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth2
from app.database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # hash password
    hashed_password = utils.hash_password(user.password)

    # create user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not utils.verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = oauth2.create_access_token(data={"user_id": db_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }