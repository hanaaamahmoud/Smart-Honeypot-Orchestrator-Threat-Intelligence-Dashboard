from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HoneypotStatus(BaseModel):
    name: str
    status: str


class CountryCount(BaseModel):
    country: str
    count: int


class StatisticsResponse(BaseModel):
    totalAttacks: int
    uniqueAttackers: int
    topCountries: List[CountryCount]


class RecentEvent(BaseModel):
    timestamp: str
    honeypot: str
    protocol: str
    source_ip: str
    country: Optional[str] = None
    attack_type: Optional[str] = None
    severity: Optional[str] = None


class TopAttacker(BaseModel):
    ip: str
    count: int


class CountryAttacks(BaseModel):
    country: str
    attacks: int


class AttackEvent(BaseModel):
    timestamp: datetime
    honeypot: str
    protocol: str

    source_ip: str
    source_port: Optional[int] = None

    destination_ip: Optional[str] = None
    destination_port: Optional[int] = None

    session_id: str

    username: Optional[str] = None
    password: Optional[str] = None

    user_attempt: int = 0
    pass_attempt: int = 0
    auth_attempt: int = 0
    anonymous: int = 0
    command_count: int = 0

    country: Optional[str] = None
    country_code: Optional[str] = None
    asn: Optional[int] = None
    ip_reputation: Optional[str] = None

    attack_type: Optional[str] = None
    mitre_technique: Optional[str] = None
    attack_stage: Optional[str] = None
    severity: Optional[str] = None

    source_dataset: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class CreateUserRequest(BaseModel):
    name: str
    email: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    organization_id: int
    status: str


class ActivateRequest(BaseModel):
    token: str
    password: str


class ResendActivationRequest(BaseModel):
    userId: int


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str