from app.db.session import SessionLocal
from app.models.db_models.organization import Organization
from app.models.db_models.user import User
from app.core.security import hash_password


DEMO_USERS = [
    {"name": "System Admin", "email": "admin@smarthoneypot.local", "password": "Admin@123456", "role": "admin"},
    {"name": "Sub Admin", "email": "subadmin@smarthoneypot.local", "password": "SubAdmin@123456", "role": "sub-admin"},
    {"name": "Security Analyst", "email": "analyst@smarthoneypot.local", "password": "Analyst@123456", "role": "analyst"},
    {"name": "Read Only User", "email": "reader@smarthoneypot.local", "password": "Reader@123456", "role": "reader"},
]


def run():
    db = SessionLocal()

    org = db.query(Organization).filter(Organization.name == "Smart Honeypot Org").first()
    if not org:
        org = Organization(name="Smart Honeypot Org")
        db.add(org)
        db.commit()
        db.refresh(org)

    admin_user = db.query(User).filter(User.email == "admin@smarthoneypot.local").first()
    if not admin_user:
        admin_user = User(
            name="System Admin",
            email="admin@smarthoneypot.local",
            password_hash=hash_password("Admin@123456"),
            role="admin",
            organization_id=org.id,
            status="active"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

    for u in DEMO_USERS:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if existing:
            existing.password_hash = hash_password(u["password"])
            existing.role = u["role"]
            existing.status = "active"
            existing.organization_id = org.id
        else:
            user = User(
                name=u["name"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                role=u["role"],
                organization_id=org.id,
                status="active",
                created_by=admin_user.id
            )
            db.add(user)

    db.commit()
    db.close()
    print("Demo users seeded successfully.")


if __name__ == "__main__":
    run()
