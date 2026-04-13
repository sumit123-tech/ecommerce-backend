from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.role_checker import admin_only
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderOut)
def place_order(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="Cart not found")

    cart_items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0

    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

        total_price += product.price * item.quantity

    new_order = models.Order(
        user_id=current_user.id,
        total_price=total_price,
        status="placed"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()

        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)

        product.stock -= item.quantity

    db.commit()

    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()

    return new_order


@router.get("/", response_model=list[schemas.OrderOut])
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
    return orders

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    allowed_status = ["placed", "confirmed", "shipped", "delivered", "cancelled"]

    if status_update.status.lower() not in allowed_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    order.status = status_update.status.lower()
    db.commit()

    return {
        "message": "Order status updated",
        "order_id": order.id,
        "new_status": order.status
    }