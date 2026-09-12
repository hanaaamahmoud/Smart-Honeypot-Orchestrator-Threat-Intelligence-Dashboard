"""
Output adapter.

Converts internal ML results into Backend-compatible output contracts.
This layer does not perform clustering, feature generation, model inference,
or backend calls.
"""

import math
from typing import Any, Dict


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None

    return value


def adapt_session_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "session_id": _sanitize_value(result["session_id"]),
        "cluster_id": _sanitize_value(result.get("cluster_id")),
        "assignment_status": _sanitize_value(result["assignment_status"]),
        "validation_status": _sanitize_value(result["validation_status"]),
        "event_count": _sanitize_value(result.get("event_count", 0)),
        "protocol": _sanitize_value(result.get("protocol")),
        "honeypot": _sanitize_value(result.get("honeypot")),
    }


def adapt_analytics_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "cluster_id": _sanitize_value(result["cluster_id"]),
        "session_count": _sanitize_value(result.get("session_count", 0)),
        "event_count": _sanitize_value(result.get("event_count", 0)),
        "top_commands": _sanitize_value(result.get("top_commands", [])),
        "attack_types": _sanitize_value(result.get("attack_types", [])),
        "mitre_techniques": _sanitize_value(
            result.get("mitre_techniques", [])
        ),
    }
