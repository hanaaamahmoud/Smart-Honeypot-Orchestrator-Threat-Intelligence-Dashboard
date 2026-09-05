from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HoneypotStatus(BaseModel):
    name: str
    status: str


class StatisticsResponse(BaseModel):
    totalAttacks: int
    activeHoneypots: int
    uniqueSources: int
    countries: int


class RecentEvent(BaseModel):
    id: int
    honeypot: str
    sourceIp: str
    country: str
    attackType: str
    timestamp: str


class TopAttacker(BaseModel):
    ip: str
    attacks: int


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