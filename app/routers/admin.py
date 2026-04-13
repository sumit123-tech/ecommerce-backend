from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models
from app.dependencies.role_checker import admin_only

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    total_users = db.query(models.User).count()
    total_products = db.query(models.Product).count()
    total_orders = db.query(models.Order).count()

    total_revenue = db.query(func.sum(models.Order.total_price)).filter(
        models.Order.payment_status == "paid"
    ).scalar()

    if total_revenue is None:
        total_revenue = 0

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }