from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/pay")
def make_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == payment.order_id,
        models.Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Order already paid")

    allowed_methods = ["cod", "upi", "card"]

    if payment.payment_method.lower() not in allowed_methods:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    order.payment_status = "paid"
    order.payment_method = payment.payment_method.lower()
    order.status = "confirmed"

    db.commit()

    return {
        "message": "Payment successful",
        "order_id": order.id,
        "payment_status": order.payment_status,
        "payment_method": order.payment_method,
        "order_status": order.status
    }