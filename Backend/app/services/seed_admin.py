from passlib.context import CryptContext
from app.db.session import SessionLocal
from app.models.db_models.organization import Organization
from app.models.db_models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def run():
    db = SessionLocal()

    org = db.query(Organization).filter(Organization.name == "Fixed Solutions").first()
    if not org:
        org = Organization(name="Fixed Solutions")
        db.add(org)
        db.commit()
        db.refresh(org)

    admin = db.query(User).filter(User.email == "admin@test.com").first()
    if not admin:
        admin = User(
            email="admin@test.com",
            password_hash=pwd_context.hash("Admin@12345"),
            name="System Admin",
            role="admin",
            organization_id=org.id,
            status="active",
        )
        db.add(admin)
        db.commit()
        print("Admin created: admin@test.com / Admin@12345")
    else:
        print("Admin already exists.")

    db.close()


if __name__ == "__main__":
    run()
