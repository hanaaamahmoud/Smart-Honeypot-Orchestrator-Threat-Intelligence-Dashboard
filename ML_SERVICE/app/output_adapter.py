"""
Output adapter.

Converts internal ML results into Backend-compatible output contracts.

The adapter accepts legacy/internal input names but always returns
the canonical backend contract.
"""

from __future__ import annotations

import math
from typing import Any, Dict


def _sanitize_value(value: Any) -> Any:
    """
    Convert NaN / +/-Infinity into None.

    Sanitize nested dictionaries/lists/tuples recursively so the
    resulting object can be serialized safely.
    """
    if isinstance(value, float):
        if not math.isfinite(value):
            return None
        return value

    if isinstance(value, dict):
        return {
            key: _sanitize_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _sanitize_value(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            _sanitize_value(item)
            for item in value
        ]

    return value


def _first_present(
    result: Dict[str, Any],
    *keys: str,
) -> Any:
    """
    Return the first explicitly present key.

    Canonical names are preferred.
    Legacy aliases are accepted as input only.
    """
    for key in keys:
        if key in result:
            return result[key]

    return None


def adapt_session_result(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an internal session result into the canonical
    backend/dashboard output contract.

    Canonical output fields:

    - reconstructed_session_id
    - production_cluster_assignment
    - assignment_status
    - feature_validation_status
    - event_count
    - session_start
    - session_end
    - source
    - protocol
    - honeypot

    Legacy/internal aliases are accepted as input:

    - session_id
    - cluster_id
    - validation_status

    The input dictionary is never modified.
    """

    if not isinstance(result, dict):
        raise TypeError("result must be a dictionary")

    reconstructed_session_id = _first_present(
        result,
        "reconstructed_session_id",
        "session_id",
    )

    production_cluster_assignment = _first_present(
        result,
        "production_cluster_assignment",
        "cluster_id",
    )

    assignment_status = _first_present(
        result,
        "assignment_status",
    )

    feature_validation_status = _first_present(
        result,
        "feature_validation_status",
        "validation_status",
    )

    if reconstructed_session_id is None:
        raise KeyError(
            "reconstructed_session_id"
        )

    if assignment_status is None:
        raise KeyError(
            "assignment_status"
        )

    if feature_validation_status is None:
        raise KeyError(
            "feature_validation_status"
        )

    return {
        "reconstructed_session_id": _sanitize_value(
            reconstructed_session_id
        ),
        "production_cluster_assignment": _sanitize_value(
            production_cluster_assignment
        ),
        "assignment_status": _sanitize_value(
            assignment_status
        ),
        "feature_validation_status": _sanitize_value(
            feature_validation_status
        ),
        "event_count": _sanitize_value(
            result.get("event_count", 0)
        ),
        "session_start": _sanitize_value(
            result.get(
                "session_start",
                result.get("start_time"),
            )
        ),
        "session_end": _sanitize_value(
            result.get(
                "session_end",
                result.get("end_time"),
            )
        ),
        "source": _sanitize_value(
            result.get("source")
        ),
        "protocol": _sanitize_value(
            result.get("protocol")
        ),
        "honeypot": _sanitize_value(
            result.get("honeypot")
        ),
    }


def adapt_analytics_result(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an internal analytics result into the canonical
    backend/dashboard output contract.
    """

    if not isinstance(result, dict):
        raise TypeError("result must be a dictionary")

    if "cluster_id" not in result:
        raise KeyError("cluster_id")

    return {
        "cluster_id": _sanitize_value(
            result["cluster_id"]
        ),
        "session_count": _sanitize_value(
            result.get("session_count", 0)
        ),
        "event_count": _sanitize_value(
            result.get("event_count", 0)
        ),
        "top_commands": _sanitize_value(
            result.get("top_commands", [])
        ),
        "attack_types": _sanitize_value(
            result.get("attack_types", [])
        ),
        "mitre_techniques": _sanitize_value(
            result.get("mitre_techniques", [])
        ),
    }
