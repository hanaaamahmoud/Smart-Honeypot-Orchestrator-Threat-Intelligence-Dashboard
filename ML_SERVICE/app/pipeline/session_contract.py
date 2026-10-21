"""
D2.1 — Session Contract

Defines the stable output contract for reconstructed sessions.

This module does NOT:
- generate behavioral features
- perform scaling
- perform clustering
- modify input events
"""

from typing import Any, Dict, List, TypedDict


class SessionContract(TypedDict):
    """
    Stable session representation produced by D2.
    """

    session_id: str
    events: List[Dict[str, Any]]
    event_count: int
    start_time: str
    end_time: str
    duration_seconds: float
