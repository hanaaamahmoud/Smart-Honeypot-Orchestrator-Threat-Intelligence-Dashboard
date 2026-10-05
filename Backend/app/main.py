import asyncio
from contextlib import asynccontextmanager
from typing import List
from collections import defaultdict

import requests

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_plain_token,
    hash_token,
    hash_password
)

from app.db.session import get_db

from app.models.db_models.user import User
from app.models.db_models.activation_token import ActivationToken
from app.models.db_models.password_reset_token import PasswordResetToken
from app.models.db_models.audit_log import AuditLog

from app.models.schemas import (
    HoneypotStatus,
    StatisticsResponse,
    RecentEvent,
    TopAttacker,
    LoginRequest,
    LoginResponse,
    CreateUserRequest,
    ActivateRequest,
    ResendActivationRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.websocket.manager import ConnectionManager
from app.websocket.producer import produce_events
from app.services.audit_service import write_audit_log

from app.services.statistics_service import (
    get_statistics,
    get_recent_events,
    get_top_attackers,
)

from app.services.live_service import (
    get_live_kpis, get_by_honeypot, get_by_protocol,
    get_by_severity, get_by_country, get_top_attackers,
    get_by_mitre, get_timeline, get_recent_events, get_by_reputation
)
# ──────────────────────────────────────────
# Rate Limiting
# ──────────────────────────────────────────

FAILED_LOGINS = defaultdict(list)
MAX_ATTEMPTS = 5
WINDOW_MINUTES = 15


def is_locked(email: str) -> bool:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=WINDOW_MINUTES)
    FAILED_LOGINS[email] = [t for t in FAILED_LOGINS[email] if t > window_start]
    return len(FAILED_LOGINS[email]) >= MAX_ATTEMPTS


def record_failed_attempt(email: str):
    FAILED_LOGINS[email].append(datetime.now(timezone.utc))


def clear_failed_attempts(email: str):
    FAILED_LOGINS[email] = []


# ──────────────────────────────────────────
# WebSocket + Lifespan
# ──────────────────────────────────────────

manager = ConnectionManager()
ORCHESTRATOR_URL = settings.ORCHESTRATOR_URL


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer_task = asyncio.create_task(produce_events(manager))
    yield
    producer_task.cancel()
    try:
        await producer_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Smart Honeypot Backend",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────
# Auth Helpers
# ──────────────────────────────────────────

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "code": "INVALID_TOKEN", "message": "Invalid or expired token."}
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "code": "INVALID_TOKEN_TYPE", "message": "Access token required."}
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "code": "INVALID_TOKEN_PAYLOAD", "message": "Invalid token payload."}
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "code": "USER_NOT_FOUND", "message": "User not found."}
        )

    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"success": False, "code": "ACCOUNT_NOT_ACTIVE", "message": "Account is not active."}
        )

    return user


def require_roles(allowed_roles: List[str]):
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"success": False, "code": "FORBIDDEN", "message": "You do not have permission to access this resource."}
            )
        return current_user
    return checker


def can_create_role(creator_role: str, target_role: str) -> bool:
    if creator_role == "admin":
        return target_role in ["sub-admin", "analyst", "reader", "admin"]
    if creator_role == "sub-admin":
        return target_role in ["analyst", "reader"]
    return False


# ──────────────────────────────────────────
# Base Routes
# ──────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Smart Honeypot Backend is running"}


@app.get("/honeypots", response_model=List[HoneypotStatus])
def get_honeypots():
    try:
        response = requests.get(f"{ORCHESTRATOR_URL}/status", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail={"success": False, "code": "ORCHESTRATOR_UNAVAILABLE", "message": "Orchestrator service is unavailable."}
        )


# ──────────────────────────────────────────
# Dashboard Routes (Elasticsearch-backed)
# ──────────────────────────────────────────

@app.get("/statistics", response_model=StatisticsResponse)
def statistics():
    try:
        return get_statistics()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/events/recent", response_model=List[RecentEvent])
def recent_events():
    try:
        return get_recent_events()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/attackers/top", response_model=List[TopAttacker])
def top_attackers():
    try:
        return get_top_attackers()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ──────────────────────────────────────────
# Auth APIs
# ──────────────────────────────────────────

@app.post("/api/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):

    if is_locked(payload.email):
        raise HTTPException(
            status_code=429,
            detail={"success": False, "code": "TOO_MANY_ATTEMPTS", "message": "Too many failed attempts. Please try again later."}
        )

    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        record_failed_attempt(payload.email)
        write_audit_log(db, "LOGIN_FAILED", request=request, details={"email": payload.email})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "code": "INVALID_CREDENTIALS", "message": "Invalid email or password."}
        )

    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"success": False, "code": "ACCOUNT_NOT_ACTIVE", "message": "Account is not active."}
        )

    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "organization_id": user.organization_id
    })

    refresh_token = create_refresh_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "organization_id": user.organization_id
    })

    clear_failed_attempts(payload.email)
    write_audit_log(db, "LOGIN_SUCCESS", request=request, user_id=user.id, details={"email": user.email})

    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "organization_id": user.organization_id,
            "status": user.status
        }
    }


@app.get("/api/auth/me")
def auth_me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "role": current_user.role,
            "organization_id": current_user.organization_id,
            "status": current_user.status
        }
    }


@app.post("/api/auth/logout")
def logout(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    write_audit_log(db, "LOGOUT", request=request, user_id=current_user.id, details={"email": current_user.email})
    return {"success": True, "message": "Logged out successfully."}


@app.post("/api/auth/activate")
def activate_account(payload: ActivateRequest, request: Request, db: Session = Depends(get_db)):

    if len(payload.password) < 8:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "code": "WEAK_PASSWORD", "message": "Password must be at least 8 characters."}
        )

    token_hash_value = hash_token(payload.token)
    token_row = db.query(ActivationToken).filter(ActivationToken.token_hash == token_hash_value).first()

    if not token_row or token_row.used_at is not None:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "code": "INVALID_ACTIVATION_TOKEN", "message": "Invalid activation link."}
        )

    if token_row.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail={"success": False, "code": "EXPIRED_ACTIVATION_TOKEN", "message": "Activation link expired."}
        )

    user = db.query(User).filter(User.id == token_row.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.status == "active":
        raise HTTPException(
            status_code=400,
            detail={"success": False, "code": "ACCOUNT_ALREADY_ACTIVATED", "message": "Account already activated."}
        )

    user.password_hash = hash_password(payload.password)
    user.status = "active"
    user.activated_at = datetime.now(timezone.utc)
    user.password_changed_at = datetime.now(timezone.utc)
    token_row.used_at = datetime.now(timezone.utc)
    db.commit()

    write_audit_log(db, "ACCOUNT_ACTIVATED", request=request, user_id=user.id, details={"email": user.email})
    return {"success": True, "message": "Account activated successfully."}


@app.post("/api/auth/resend-activation")
def resend_activation(
    payload: ResendActivationRequest,
    request: Request,
    current_user: User = Depends(require_roles(["admin", "sub-admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == payload.userId).first()

    if not user:
        raise HTTPException(status_code=404, detail={"success": False, "code": "USER_NOT_FOUND", "message": "User not found."})

    if user.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail={"success": False, "code": "FORBIDDEN", "message": "You do not have permission to access this resource."})

    if user.status == "active":
        raise HTTPException(status_code=400, detail={"success": False, "code": "ACCOUNT_ALREADY_ACTIVATED", "message": "Account already activated."})

    old_tokens = db.query(ActivationToken).filter(
        ActivationToken.user_id == user.id,
        ActivationToken.used_at.is_(None)
    ).all()
    for t in old_tokens:
        t.used_at = datetime.now(timezone.utc)

    plain_token = generate_plain_token()
    new_token = ActivationToken(
        user_id=user.id,
        token_hash=hash_token(plain_token),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30)
    )
    db.add(new_token)
    db.commit()

    write_audit_log(db, "ACTIVATION_RESEND", request=request, user_id=current_user.id, details={"target_user_id": user.id, "target_email": user.email})

    return {
        "success": True,
        "message": "Activation link resent successfully.",
        "activation_token_for_testing": plain_token
    }


@app.post("/api/auth/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    generic_response = {"success": True, "message": "If this email exists, a password reset link has been sent."}

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return generic_response

    old_tokens = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used_at.is_(None)
    ).all()
    for t in old_tokens:
        t.used_at = datetime.now(timezone.utc)

    plain_token = generate_plain_token()
    token_row = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_token(plain_token),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30)
    )
    db.add(token_row)
    db.commit()

    write_audit_log(db, "PASSWORD_RESET_REQUESTED", request=request, user_id=user.id, details={"email": user.email})

    return {**generic_response, "reset_token_for_testing": plain_token}


@app.post("/api/auth/reset-password")
def reset_password(payload: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):

    if len(payload.password) < 8:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "code": "WEAK_PASSWORD", "message": "Password must be at least 8 characters."}
        )

    token_hash_value = hash_token(payload.token)
    token_row = db.query(PasswordResetToken).filter(PasswordResetToken.token_hash == token_hash_value).first()

    if not token_row or token_row.used_at is not None:
        raise HTTPException(status_code=400, detail={"success": False, "code": "INVALID_RESET_TOKEN", "message": "Invalid reset link."})

    if token_row.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail={"success": False, "code": "EXPIRED_RESET_TOKEN", "message": "Reset link expired."})

    user = db.query(User).filter(User.id == token_row.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(payload.password)
    user.password_changed_at = datetime.now(timezone.utc)
    token_row.used_at = datetime.now(timezone.utc)
    db.commit()

    write_audit_log(db, "PASSWORD_CHANGED", request=request, user_id=user.id, details={"email": user.email})
    return {"success": True, "message": "Password reset successfully."}


# ──────────────────────────────────────────
# User Management APIs
# ──────────────────────────────────────────

@app.post("/api/users")
def create_user(
    payload: CreateUserRequest,
    request: Request,
    current_user: User = Depends(require_roles(["admin", "sub-admin"])),
    db: Session = Depends(get_db)
):
    if not can_create_role(current_user.role, payload.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"success": False, "code": "FORBIDDEN_ROLE_CREATION", "message": "You do not have permission to create this role."}
        )

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "code": "EMAIL_ALREADY_EXISTS", "message": "Email already in use."}
        )

    new_user = User(
        name=payload.name,
        email=payload.email,
        role=payload.role,
        organization_id=current_user.organization_id,
        status="pending",
        password_hash=None,
        created_by=current_user.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    old_tokens = db.query(ActivationToken).filter(
        ActivationToken.user_id == new_user.id,
        ActivationToken.used_at.is_(None)
    ).all()
    for t in old_tokens:
        t.used_at = datetime.now(timezone.utc)

    plain_token = generate_plain_token()
    activation = ActivationToken(
        user_id=new_user.id,
        token_hash=hash_token(plain_token),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30)
    )
    db.add(activation)
    db.commit()

    write_audit_log(db, "USER_CREATED", request=request, user_id=current_user.id, details={
        "new_user_id": new_user.id,
        "new_user_email": new_user.email,
        "new_user_role": new_user.role
    })

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
        "organization_id": new_user.organization_id,
        "status": new_user.status,
        "activation_token_for_testing": plain_token
    }


# ──────────────────────────────────────────
# Audit Logs API
# ──────────────────────────────────────────

@app.get("/api/audit-logs")
def get_audit_logs(
    current_user: User = Depends(require_roles(["admin", "sub-admin"])),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)

    if current_user.role != "admin":
        query = query.filter(
            (AuditLog.user_id == current_user.id) | (AuditLog.user_id.is_(None))
        )

    logs = query.order_by(AuditLog.timestamp.desc()).limit(100).all()

    return {
        "success": True,
        "count": len(logs),
        "items": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "timestamp": log.timestamp,
                "details": log.details
            }
            for log in logs
        ]
    }


# ──────────────────────────────────────────
# Test Routes
# ──────────────────────────────────────────

@app.get("/api/admin-only")
def admin_only_route(current_user: User = Depends(require_roles(["admin"]))):
    return {"success": True, "message": f"Welcome Admin {current_user.email}"}


@app.get("/api/analysis")
def analysis_route(current_user: User = Depends(require_roles(["admin", "sub-admin", "analyst"]))):
    return {"success": True, "message": f"Analysis access granted for role: {current_user.role}"}


# ___________________________________

@app.get("/api/live/kpis")
def live_kpis():
    try:
        return get_live_kpis()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/by-honeypot")
def live_by_honeypot():
    try:
        return get_by_honeypot()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/by-protocol")
def live_by_protocol():
    try:
        return get_by_protocol()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/by-severity")
def live_by_severity():
    try:
        return get_by_severity()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/by-country")
def live_by_country():
    try:
        return get_by_country()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/top-attackers")
def live_top_attackers():
    try:
        return get_top_attackers()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/by-mitre")
def live_by_mitre():
    try:
        return get_by_mitre()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))



@app.get("/api/live/timeline")
def live_timeline():
    try:
        return get_timeline()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/recent")
def live_recent():
    try:
        return get_recent_events()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/live/by-reputation")
def live_by_reputation():
    try:
        return get_by_reputation()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))