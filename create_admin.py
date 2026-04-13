from app.database import SessionLocal
from app import models, utils

db = SessionLocal()

admin_email = "admin@gmail.com"
admin_password = "123456"

existing_admin = db.query(models.User).filter(models.User.email == admin_email).first()

if existing_admin:
    print("Admin already exists")
else:
    hashed_password = utils.hash_password(admin_password)

    new_admin = models.User(
        name="Admin",
        email=admin_email,
        password=hashed_password,
        role="admin"
    )

    db.add(new_admin)
    db.commit()
    print("Admin created successfully")

db.close()