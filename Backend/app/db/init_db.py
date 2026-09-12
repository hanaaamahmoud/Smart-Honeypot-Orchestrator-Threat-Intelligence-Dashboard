from app.db.session import Base, engine
from app.models.db_models import Organization, User, ActivationToken, PasswordResetToken, AuditLog  # noqa


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("DB tables created successfully.")
