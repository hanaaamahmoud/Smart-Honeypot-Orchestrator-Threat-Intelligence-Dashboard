from app.db.session import SessionLocal
from app.models.db_models.user import User
from app.core.security import hash_password


def run():
    db = SessionLocal()
    user = db.query(User).filter(User.email == "admin@test.com").first()
    if not user:
        print("admin@test.com not found")
        return

    user.password_hash = hash_password("Admin@12345")
    user.status = "active"
    db.commit()
    print("Admin password reset successfully.")
    db.close()


if __name__ == "__main__":
    run()