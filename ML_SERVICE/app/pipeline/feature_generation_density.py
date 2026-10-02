"""
D3.5 — Log / Density Feature Generation

Generates log-transformed and density behavioral features.

COLAB PARITY NOTE
-----------------
Mirrors the original Colab Step 5B-2 exactly:

    session_duration_log1p          = log1p(session_duration_recomputed_seconds)
    event_count_log1p               = log1p(event_count)
    inter_event_gap_mean_log1p      = log1p(inter_event_gap_mean)
    inter_event_gap_max_log1p       = log1p(inter_event_gap_max)

    event_density                   = event_count / duration      (0 if duration <= 0)
    command_density                 = command_count_total / event_count   (0 if event_count <= 0)
    auth_attempt_density            = auth_attempt_total / event_count   (0 if event_count <= 0)
    credential_attempt_density      = (user_attempt_total + pass_attempt_total) / event_count  (0 if event_count <= 0)

Note: Only ``event_density`` divides by duration. The other
densities divide by ``event_count``.

This module does NOT:
- scale features
- cluster
- modify input sessions
- assemble the final 48-feature vector
"""

from copy import deepcopy
from math import isfinite, log1p
from typing import Any, Dict, Optional


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


def _density_over_duration(
    numerator: Any,
    duration: Any,
    numerator_name: str,
) -> float:
    """
    Numerator / duration, with 0.0 when duration <= 0.
    Used for ``event_density`` only.
    """
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

    if duration_value == 0.0:
        return 0.0

    result = numerator_value / duration_value

    if not isfinite(result):
        raise ValueError(
            f"{numerator_name} density is non-finite"
        )

    return float(result)


def _density_over_event_count(
    numerator: Any,
    event_count: Any,
    numerator_name: str,
) -> float:
    """
    Numerator / event_count, with 0.0 when event_count <= 0.
    Used for command / auth / credential densities
    (Colab parity).
    """
    numerator_value = _safe_float(
        numerator,
        numerator_name,
    )

    event_count_value = _safe_float(
        event_count,
        "event_count",
    )

    if numerator_value < 0:
        raise ValueError(
            f"{numerator_name} cannot be negative"
        )

    if event_count_value < 0:
        raise ValueError(
            "event_count cannot be negative"
        )

    if event_count_value == 0.0:
        return 0.0

    result = numerator_value / event_count_value

    if not isfinite(result):
        raise ValueError(
            f"{numerator_name} density is non-finite"
        )

    return float(result)


def generate_density_features(
    session_or_base: Dict[str, Any],
    temporal_features: Optional[Dict[str, Any]] = None,
) -> Dict[str, float]:
    """
    Generate D3.5 log and density features.

    Supported call forms:

        generate_density_features(session)

    or, for staged feature generation:

        generate_density_features(base, temporal)

    In the two-argument form, the feature dictionaries are merged
    without modifying either input.
    """

    if not isinstance(session_or_base, dict):
        raise TypeError("session_or_base must be a dictionary")

    if temporal_features is not None:
        if not isinstance(temporal_features, dict):
            raise TypeError("temporal_features must be a dictionary")

        copied_session = deepcopy(session_or_base)
        copied_session.update(
            deepcopy(temporal_features)
        )
    else:
        copied_session = deepcopy(session_or_base)

    duration = copied_session.get(
        "duration_seconds",
        copied_session.get(
            "session_duration_seconds",
            copied_session.get(
                "session_duration_recomputed_seconds",
                0.0,
            ),
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

    user_attempt_total = copied_session.get(
        "user_attempt_total",
        0,
    )

    pass_attempt_total = copied_session.get(
        "pass_attempt_total",
        0,
    )

    credential_attempt_total = (
        user_attempt_total + pass_attempt_total
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

        # Colab parity: event_density divides by duration.
        "event_density": _density_over_duration(
            event_count,
            duration,
            "event_count",
        ),

        # Colab parity: the three densities below divide by
        # event_count, not duration.
        "command_density": _density_over_event_count(
            command_count,
            event_count,
            "command_count_total",
        ),

        "auth_attempt_density": _density_over_event_count(
            auth_attempt_total,
            event_count,
            "auth_attempt_total",
        ),

        "credential_attempt_density": _density_over_event_count(
            credential_attempt_total,
            event_count,
            "credential_attempt_total",
        ),
    }
