"""Boundary adapter from production session results to analytics input."""

from __future__ import annotations

from typing import Any, Iterable


def _cluster_representation(cluster_id: int | None) -> str:
    """
    Convert the production numeric cluster assignment into the
    analytics contract representation.

    This does not modify the production result.
    """

    if cluster_id is None:
        return "NOISE"

    return "EXISTING_PRODUCTION_CLUSTER"


def build_session_analytics_input(
    results: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Adapt existing production session results for SESSION_ANALYTICS.

    The original production records are not mutated.
    """

    output: list[dict[str, Any]] = []

    for record in results:
        if not isinstance(record, dict):
            raise TypeError(
                "Each production session result must be a dictionary"
            )

        row = dict(record)

        cluster_id = row.get(
            "production_cluster_assignment"
        )

        row["production_cluster_assignment"] = (
            _cluster_representation(cluster_id)
        )

        output.append(row)

    return output


__all__ = [
    "build_session_analytics_input",
]
