from fastapi import FastAPI, Depends
from app.database import engine, Base
from app import models, oauth2
from app.routers import auth, categories, products, cart, orders, payments, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Server is running successfully 🚀"}


@app.get("/me")
def get_me(current_user=Depends(oauth2.get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }