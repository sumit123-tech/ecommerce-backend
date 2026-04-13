# 🛒 E-Commerce Backend API (FastAPI)

A fully functional backend system for an e-commerce application built using FastAPI.

---

## 🚀 Features

### 👤 User
- Signup & Login (JWT Authentication)
- View products
- Add to cart
- Place order
- Make payment

### 🛠️ Admin
- Product CRUD (Create, Update, Delete)
- Category management
- Order status update (shipped, delivered)
- Admin dashboard (users, orders, revenue)

---

## ⚙️ Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- SQLite
- JWT Authentication
- Docker

---

## 🔐 Authentication

- Secure login using JWT tokens
- Role-based access (Admin / Customer)

---

## 📦 API Endpoints

### Auth
- POST `/signup`
- POST `/login`

### Products
- GET `/products/`
- POST `/products/` (Admin only)
- PUT `/products/{id}` (Admin only)
- DELETE `/products/{id}` (Admin only)

### Cart
- POST `/cart/add`
- GET `/cart/`
- DELETE `/cart/remove`

### Orders
- POST `/orders/`
- GET `/orders/`
- PUT `/orders/{id}/status` (Admin only)

### Payments
- POST `/payments/pay`

### Admin
- GET `/admin/dashboard`

---

## 🧪 API Testing

Swagger UI available at:
http://localhost:8000/docs


---

## 🐳 Docker Setup

### Build Image
docker build -t ecommerce-api .

### Run Container
docker run -p 8000:8000 ecommerce-api


---

## 🌐 Deployment

Deployed using Render (or ready for deployment)

---

## 📊 Project Flow

User → Cart → Order → Payment → Order Confirmed

---

## 🧠 Author

Sumit Banerjee  
B.Tech CSE (Final Year)

---

## ⭐ Notes

This project demonstrates a real-world backend architecture with authentication, role-based access, and scalable API design.
