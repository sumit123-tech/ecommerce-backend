from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing_category = db.query(models.Category).filter(models.Category.name == category.name).first()

    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=list[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories