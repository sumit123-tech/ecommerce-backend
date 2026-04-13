from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add")
def add_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()

    if not cart:
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    existing_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == item.product_id
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + item.quantity

        if product.stock < new_quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        existing_item.quantity = new_quantity
        db.commit()
        db.refresh(existing_item)

        return {"message": "Cart item quantity updated"}

    new_item = models.CartItem(
        cart_id=cart.id,
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {"message": "Product added to cart"}


@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()

    if not cart:
        return {"cart_items": [], "total_price": 0}

    cart_items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).all()

    result = []
    total_price = 0

    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        subtotal = product.price * item.quantity
        total_price += subtotal

        result.append({
            "product_id": product.id,
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "cart_items": result,
        "total_price": total_price
    }

@router.delete("/remove/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in cart")

    db.delete(cart_item)
    db.commit()

    return {"message": "Item removed from cart"}