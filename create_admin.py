from app.database.session import SessionLocal
from app.models.employee import Employee
from app.core.security import hash_password
import os


db = SessionLocal()
admin_password = os.getenv("ADMIN_PASSWORD")
if not admin_password:
    raise RuntimeError("Defina ADMIN_PASSWORD no ambiente antes de criar o administrador.")

admin = Employee(
    name=os.getenv("ADMIN_NAME", "Administrador"),
    username=os.getenv("ADMIN_USERNAME", "admin"),
    password_hash=hash_password(admin_password),
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
