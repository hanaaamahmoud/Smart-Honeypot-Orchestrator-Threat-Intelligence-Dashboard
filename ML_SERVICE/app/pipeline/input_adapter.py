"""
D5.2 — Input Adapter

Provides a source-neutral boundary between external input
and the existing normalization pipeline.
"""

from typing import Any, Dict, List

from app.pipeline.normalization import normalize_events


def adapt_input(
    payload: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Adapt an external payload into the normalized event stream.

    Expected input:

        {
            "events": [...]
        }

    The adapter does not calculate features or modify the ML
    pipeline. It only extracts the events and passes them to
    normalize_events().
    """

    if not isinstance(payload, dict):
        raise TypeError(
            "Input payload must be a dictionary"
        )

    if "events" not in payload:
        raise ValueError(
            "Input payload must contain 'events'"
        )

    events = payload["events"]

    if not isinstance(events, list):
        raise TypeError(
            "Input payload 'events' must be a list"
        )

    return normalize_events(events)
