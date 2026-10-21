import json
from fastapi import Request
from sqlalchemy.orm import Session
from app.models.db_models.audit_log import AuditLog


def write_audit_log(
    db: Session,
    action: str,
    request: Request = None,
    user_id: int = None,
    details: dict = None
):
    ip = request.client.host if request and request.client else None
    ua = request.headers.get("user-agent") if request else None

    row = AuditLog(
        user_id=user_id,
        action=action,
        ip_address=ip,
        user_agent=ua,
        details=json.dumps(details or {})
    )
    db.add(row)
    db.commit()
