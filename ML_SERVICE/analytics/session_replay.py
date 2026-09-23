"""
SESSION_REPLAY

Core session replay analytics contract.

Current status:
    DEFERRED

The implementation must not fabricate session identifiers or
assume that the current Real ELK dataset satisfies the contract.
"""

from typing import Any, Dict, List


class SessionReplayDeferredError(RuntimeError):
    """Raised when SESSION_REPLAY is invoked before ML output is available."""


def build_session_replay(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build Core SESSION_REPLAY output.

    DEFERRED:
    Actual implementation is intentionally not enabled until the
    contracted ML event output is available.
    """
    raise SessionReplayDeferredError(
        "SESSION_REPLAY is DEFERRED until the contracted ML event output "
        "is available."
    )
