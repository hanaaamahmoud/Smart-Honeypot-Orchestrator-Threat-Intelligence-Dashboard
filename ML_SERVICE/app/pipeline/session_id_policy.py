"""
D2.2 — Session ID Policy

Defines how session IDs are handled during session reconstruction.

Rules:
1. Preserve an existing session_id exactly as provided.
2. Never fabricate a session_id.
3. Missing/empty session IDs are represented as None.
4. This module does not group events or mutate input.
"""

from typing import Any, Mapping, Optional


def get_session_id(event: Mapping[str, Any]) -> Optional[str]:
    """
    Return the existing session_id without fabricating one.

    Returns:
        str:
            Existing non-empty session ID.
        None:
            If session_id is missing, None, or empty.

    Raises:
        TypeError:
            If the provided session_id is not a string.
    """

    session_id = event.get("session_id")

    if session_id is None:
        return None

    if not isinstance(session_id, str):
        raise TypeError(
            "session_id must be a string when provided"
        )

    session_id = session_id.strip()

    if not session_id:
        return None

    return session_id
