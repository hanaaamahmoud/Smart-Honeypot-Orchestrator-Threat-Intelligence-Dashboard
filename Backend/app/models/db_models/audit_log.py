from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Text
from app.db.session import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    ip_address = Column(String(64), nullable=True)
    user_agent = Column(String(255), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    details = Column(Text, nullable=True)
