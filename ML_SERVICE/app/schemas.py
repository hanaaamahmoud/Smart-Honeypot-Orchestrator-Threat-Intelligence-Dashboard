"""
Production API schemas.

The schemas define the boundary of the ML service.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadinessResponse(BaseModel):
    status: str = "ready"
    ready: bool
    model_loaded: bool
    scaler_loaded: bool
    feature_contract_loaded: bool
    reference_clusters_loaded: bool


class CanonicalEvent(BaseModel):
    timestamp: str
    honeypot: str
    protocol: str
    source_ip: str
    source_port: Optional[int] = None
    destination_ip: Optional[str] = None
    destination_port: Optional[int] = None
    session_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    user_attempt: Optional[int] = None
    pass_attempt: Optional[int] = None
    auth_attempt: Optional[int] = None
    anonymous: Optional[int] = None
    command_count: Optional[int] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    asn: Optional[int] = None
    ip_reputation: Optional[str] = None
    attack_type: Optional[str] = None
    mitre_technique: Optional[str] = None
    attack_stage: Optional[str] = None
    severity: Optional[str] = None
    source_dataset: Optional[str] = None


class SessionResult(BaseModel):
    reconstructed_session_id: str

    production_cluster_assignment: Optional[int] = None

    assignment_status: str

    feature_validation_status: str

    event_count: int = 0

    session_start: Optional[str] = None

    session_end: Optional[str] = None

    source: Optional[str] = None

    protocol: Optional[str] = None

    honeypot: Optional[str] = None


class AnalyticsResult(BaseModel):
    cluster_id: int

    session_count: int = 0

    event_count: int = 0

    top_commands: List[str] = Field(
        default_factory=list
    )

    attack_types: List[str] = Field(
        default_factory=list
    )

    mitre_techniques: List[str] = Field(
        default_factory=list
    )


class ProcessRequest(BaseModel):
    events: List[Dict[str, Any]]


class ProcessResponse(BaseModel):
    status: str

    sessions_processed: int

    results: List[SessionResult]
