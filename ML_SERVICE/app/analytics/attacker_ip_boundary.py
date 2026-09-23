"""Boundary adapter for ATTACKER_IP_ANALYTICS."""

from __future__ import annotations

from typing import Any, Iterable


def build_attacker_ip_analytics_input(
    results: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Build ATTACKER_IP_ANALYTICS input directly from production results.

    This boundary:
    - preserves existing values
    - preserves ML assignment context
    - does not perform GeoIP lookups
    - does not infer enrichment
    - does not mutate input
    """

    results = list(results)
    output: list[dict[str, Any]] = []

    for result in results:
        if not isinstance(result, dict):
            raise TypeError(
                "Each production result must be a dictionary"
            )

        # Copy only. Never mutate the production result.
        row = dict(result)

        # Preserve production assignment explicitly.
        row["production_cluster_assignment"] = result.get(
            "production_cluster_assignment"
        )

        row["reconstructed_session_id"] = result.get(
            "reconstructed_session_id"
        )

        output.append(row)

    return output


__all__ = [
    "build_attacker_ip_analytics_input",
]
