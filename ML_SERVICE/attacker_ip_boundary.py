"""Boundary adapter for ATTACKER_IP_ANALYTICS."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable


def build_attacker_ip_analytics_input(
    results: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Adapt existing production ML/event results to ATTACKER_IP_ANALYTICS.

    This boundary:
    - does not perform GeoIP lookup
    - does not call external providers
    - does not infer enrichment
    - does not modify production assignments
    - does not depend on SESSION_ANALYTICS or CLUSTER_ANALYTICS
    """

    output: list[dict[str, Any]] = []

    for result in results:
        if not isinstance(result, dict):
            raise TypeError(
                "Each production result must be a dictionary"
            )

        output.append(deepcopy(result))

    return output


__all__ = [
    "build_attacker_ip_analytics_input",
]
