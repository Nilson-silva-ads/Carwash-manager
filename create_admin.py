from app.database.session import SessionLocal
from app.models.employee import Employee
from app.core.security import hash_password


db = SessionLocal()

admin = Employee(
    name="Nilson",
    username="nilsonADM",
    password_hash=hash_password("12345"),
    is_admin=True,
    is_active=True,
)

db.add(admin)
db.commit()
db.refresh(admin)

print(f"Admin criado com ID: {admin.id}")
print(f"Username: {admin.username}")
print(f"Admin: {admin.is_admin}")

db.close()