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


class SessionResult(BaseModel):
    session_id: str

    cluster_id: Optional[int] = None

    assignment_status: str

    validation_status: str

    event_count: int = 0

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
