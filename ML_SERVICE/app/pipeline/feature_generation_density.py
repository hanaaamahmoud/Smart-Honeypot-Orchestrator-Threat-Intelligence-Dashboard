"""
D3.5 — Log / Density Feature Generation

Generates log-transformed and density behavioral features.

Features:
    session_duration_log1p
    event_count_log1p
    inter_event_gap_mean_log1p
    inter_event_gap_max_log1p
    event_density
    command_density
    auth_attempt_density
    credential_attempt_density

This module does NOT:
- scale features
- cluster
- modify input sessions
- assemble the final 48-feature vector
"""

from copy import deepcopy
from math import isfinite, log1p
from typing import Any, Dict


def _safe_float(value: Any, field_name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"{field_name} must be numeric"
        ) from exc

    if not isfinite(result):
        raise ValueError(
            f"{field_name} must be finite"
        )

    return result


def _log1p_non_negative(
    value: Any,
    field_name: str,
) -> float:
    numeric_value = _safe_float(
        value,
        field_name,
    )

    if numeric_value < 0:
        raise ValueError(
            f"{field_name} cannot be negative"
        )

    result = log1p(numeric_value)

    if not isfinite(result):
        raise ValueError(
            f"{field_name} produced a non-finite value"
        )

    return float(result)


def _density(
    numerator: Any,
    duration: Any,
    numerator_name: str,
) -> float:
    numerator_value = _safe_float(
        numerator,
        numerator_name,
    )

    duration_value = _safe_float(
        duration,
        "session_duration_seconds",
    )

    if numerator_value < 0:
        raise ValueError(
            f"{numerator_name} cannot be negative"
        )

    if duration_value < 0:
        raise ValueError(
            "session_duration_seconds cannot be negative"
        )

    # A zero-duration session cannot have a meaningful
    # rate/density. Contract policy: return 0.0.
    if duration_value == 0.0:
        return 0.0

    result = numerator_value / duration_value

    if not isfinite(result):
        raise ValueError(
            f"{numerator_name} density is non-finite"
        )

    return float(result)


def generate_density_features(
    session: Dict[str, Any],
) -> Dict[str, float]:
    """
    Generate D3.5 log and density features for one session.
    """

    if not isinstance(session, dict):
        raise TypeError("session must be a dictionary")

    copied_session = deepcopy(session)

    duration = copied_session.get(
        "duration_seconds",
        copied_session.get(
            "session_duration_seconds",
            0.0,
        ),
    )

    event_count = copied_session.get(
        "event_count",
        len(copied_session.get("events", [])),
    )

    inter_event_gap_mean = copied_session.get(
        "inter_event_gap_mean",
        0.0,
    )

    inter_event_gap_max = copied_session.get(
        "inter_event_gap_max",
        0.0,
    )

    command_count = copied_session.get(
        "command_count_total",
        0,
    )

    auth_attempt_total = copied_session.get(
        "auth_attempt_total",
        0,
    )

    credential_attempt_total = copied_session.get(
        "credential_attempt_total",
        copied_session.get(
            "user_attempt_total",
            0,
        ),
    )

    return {
        "session_duration_log1p": _log1p_non_negative(
            duration,
            "session_duration_seconds",
        ),

        "event_count_log1p": _log1p_non_negative(
            event_count,
            "event_count",
        ),

        "inter_event_gap_mean_log1p": _log1p_non_negative(
            inter_event_gap_mean,
            "inter_event_gap_mean",
        ),

        "inter_event_gap_max_log1p": _log1p_non_negative(
            inter_event_gap_max,
            "inter_event_gap_max",
        ),

        "event_density": _density(
            event_count,
            duration,
            "event_count",
        ),

        "command_density": _density(
            command_count,
            duration,
            "command_count_total",
        ),

        "auth_attempt_density": _density(
            auth_attempt_total,
            duration,
            "auth_attempt_total",
        ),

        "credential_attempt_density": _density(
            credential_attempt_total,
            duration,
            "credential_attempt_total",
        ),
    }
