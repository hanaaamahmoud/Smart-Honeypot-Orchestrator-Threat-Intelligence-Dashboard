"""Boundary adapter from production session results to analytics input.

The production result already contains:
  - production_cluster_assignment: int (numeric cluster ID)
  - assignment_status: str ("EXISTING_PRODUCTION_CLUSTER" or "NOISE")

This boundary preserves both fields unchanged. It does not
re-derive or overwrite them.
"""

from __future__ import annotations

from typing import Any, Iterable


def build_session_analytics_input(
    results: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Adapt production session results for SESSION_ANALYTICS.

    The original production records are not mutated.

    Required fields already present in each result:
      - reconstructed_session_id
      - production_cluster_assignment (int)
      - assignment_status (str)
      - feature_validation_status (str)
    """

    output: list[dict[str, Any]] = []

    for record in results:
        if not isinstance(record, dict):
            raise TypeError(
                "Each production session result must be a dictionary"
            )

        # Copy only. Never mutate.
        row = dict(record)

        # Ensure required fields exist as expected.
        if "reconstructed_session_id" not in row:
            raise ValueError(
                "Missing reconstructed_session_id in "
                "production session result"
            )

        if "production_cluster_assignment" not in row:
            raise ValueError(
                "Missing production_cluster_assignment in "
                "production session result"
            )

        if "assignment_status" not in row:
            raise ValueError(
                "Missing assignment_status in "
                "production session result"
            )

        output.append(row)

    return output


__all__ = [
    "build_session_analytics_input",
]
