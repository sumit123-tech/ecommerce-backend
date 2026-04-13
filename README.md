🛒 E-Commerce Backend API (FastAPI)

A scalable and production-ready backend system for an e-commerce application built using FastAPI, featuring authentication, role-based access, and complete order lifecycle management.

🚀 Live API

👉 https://ecommerce-backend-qdcx.onrender.com/docs

🚀 Features
👤 User
Signup & Login (JWT Authentication)
Browse products
Add/remove items from cart
Place orders
Simulated payment system
🛠️ Admin
Product CRUD (Create, Update, Delete)
Category management
Inventory control
Order status updates (pending → shipped → delivered)
Admin dashboard (users, orders, revenue)
⚙️ Tech Stack
FastAPI
SQLAlchemy (ORM)
SQLite (for development)
JWT Authentication
Docker
Render (Deployment)
🔐 Authentication & Authorization
Secure authentication using JWT tokens
Role-based access control (Admin / Customer)
Protected routes for admin operations
📦 API Endpoints
🔑 Auth
POST /signup
POST /login
📦 Products
GET /products/
POST /products/ (Admin only)
PUT /products/{id} (Admin only)
DELETE /products/{id} (Admin only)
🛒 Cart
POST /cart/add
GET /cart/
DELETE /cart/remove
📑 Orders
POST /orders/
GET /orders/
PUT /orders/{id}/status (Admin only)
💳 Payments
POST /payments/pay (Simulated)
🧑‍💼 Admin
GET /admin/dashboard
🧪 API Testing

Swagger UI (Interactive API Docs):

Local: http://localhost:8000/docs
Live: https://ecommerce-backend-qdcx.onrender.com/docs
🐳 Docker Setup
Build Image
docker build -t ecommerce-api .
Run Container
docker run -p 8000:8000 ecommerce-api
🌐 Deployment
Deployed on Render
Publicly accessible REST APIs
Ready for frontend integration
📊 System Flow
User → Cart → Order → Payment → Order Confirmed
🧠 Key Highlights
Modular FastAPI architecture using routers
Clean database design with SQLAlchemy ORM
JWT-based authentication & authorization
Real-world e-commerce workflow implementation
Dockerized for consistent deployment
Live hosted API for real-world usage
🧠 Future Improvements
PostgreSQL integration for persistent database
Real payment gateway integration (Razorpay/Stripe)
Order tracking system
Email notifications
Frontend (React) integration
👨‍💻 Author

Sumit Banerjee
B.Tech CSE (Final Year)

⭐ Project Insight

This project demonstrates a real-world backend system with scalable architecture, secure authentication, and complete business logic for an e-commerce platform — making it suitable for production-level applications.
