from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies.role_checker import admin_only

router = APIRouter(prefix="/products", tags=["Products"])


# 🔐 ADMIN ONLY
@router.post("/", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    category = db.query(models.Category).filter(models.Category.id == product.category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# 🔓 PUBLIC
@router.get("/", response_model=list[schemas.ProductOut])
def get_products(
    db: Session = Depends(get_db),
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(models.Product)

    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))

    if category_id:
        query = query.filter(models.Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    return query.offset(skip).limit(limit).all()


# 🔓 PUBLIC
@router.get("/{id}", response_model=schemas.ProductOut)
def get_single_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# 🔐 ADMIN ONLY
@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(
    id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category = db.query(models.Category).filter(models.Category.id == updated_product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product_query.update(
        {
            "name": updated_product.name,
            "description": updated_product.description,
            "price": updated_product.price,
            "stock": updated_product.stock,
            "category_id": updated_product.category_id
        },
        synchronize_session=False
    )
    db.commit()

    return product_query.first()


# 🔐 ADMIN ONLY
@router.delete("/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Product deleted successfully"}