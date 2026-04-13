from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CategoryCreate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    category_id: int


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int
    category_id: int

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    order_id: int
    payment_method: str

class OrderStatusUpdate(BaseModel):
    status: str