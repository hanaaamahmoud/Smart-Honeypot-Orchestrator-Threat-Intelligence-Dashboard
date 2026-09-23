"""Cluster analytics adapter for validated production cluster assignments."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable


REQUIRED_FIELDS = (
    "reconstructed_session_id",
    "production_cluster_assignment",
    "assignment_status",
)

OPTIONAL_FIELDS = (
    "nearest_behavioral_cluster",
    "nearest_behavioral_distance",
    "event_count",
    "session_start",
    "session_end",
    "protocol",
    "honeypot",
    "source",
    "source_ip",
)

OUTPUT_FIELDS = (
    "analytics_layer",
    "cluster_count",
    "session_count",
    "noise_session_count",
    "clusters",
)

NOISE_CLUSTER_ID = -1


def _validate_record(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError(
            "Each cluster analytics input must be a dictionary"
        )

    missing = [
        field
        for field in REQUIRED_FIELDS
        if field not in record
    ]

    if missing:
        raise ValueError(
            f"Missing required cluster analytics fields: {missing}"
        )

    null_required = [
        field
        for field in REQUIRED_FIELDS
        if record[field] is None
    ]

    if null_required:
        raise ValueError(
            "Required cluster analytics fields cannot be null: "
            f"{null_required}"
        )

    session_id = record["reconstructed_session_id"]

    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError(
            "reconstructed_session_id must be a non-empty string"
        )

    cluster_id = record["production_cluster_assignment"]

    if isinstance(cluster_id, bool) or not isinstance(cluster_id, int):
        raise ValueError(
            "production_cluster_assignment must be an integer"
        )

    assignment_status = record["assignment_status"]

    if not isinstance(assignment_status, str):
        raise TypeError(
            "assignment_status must be a string"
        )

    if not assignment_status.strip():
        raise ValueError(
            "assignment_status cannot be empty"
        )


def build_cluster_analytics(
    results: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """
    Build aggregate cluster analytics from existing production assignments.

    This layer:
    - consumes existing production assignments
    - does not fit DBSCAN
    - does not retrain the model
    - does not create clusters
    - does not modify assignments
    - does not depend on session analytics
    - does not perform GeoIP enrichment
    """

    records = list(results)

    validated_records: list[dict[str, Any]] = []
    seen_sessions: set[str] = set()

    for record in records:
        _validate_record(record)

        session_id = record["reconstructed_session_id"]

        if session_id in seen_sessions:
            raise ValueError(
                "Duplicate reconstructed_session_id in "
                "cluster analytics input: "
                f"{session_id}"
            )

        seen_sessions.add(session_id)

        # Keep analytics read-only.
        validated_records.append(
            deepcopy(record)
        )

    session_count = len(validated_records)

    if session_count == 0:
        return {
            "analytics_layer": "CLUSTER_ANALYTICS",
            "cluster_count": 0,
            "session_count": 0,
            "noise_session_count": 0,
            "clusters": [],
        }

    cluster_sessions: dict[int, int] = {}

    for record in validated_records:
        cluster_id = record[
            "production_cluster_assignment"
        ]

        cluster_sessions[cluster_id] = (
            cluster_sessions.get(cluster_id, 0) + 1
        )

    noise_session_count = cluster_sessions.get(
        NOISE_CLUSTER_ID,
        0,
    )

    behavioral_cluster_ids = sorted(
        cluster_id
        for cluster_id in cluster_sessions
        if cluster_id != NOISE_CLUSTER_ID
    )

    clusters: list[dict[str, Any]] = []

    for cluster_id in behavioral_cluster_ids:
        count = cluster_sessions[cluster_id]

        clusters.append(
            {
                "cluster_id": cluster_id,
                "session_count": count,
                "percentage": (
                    count / session_count * 100.0
                ),
            }
        )

    return {
        "analytics_layer": "CLUSTER_ANALYTICS",
        "cluster_count": len(behavioral_cluster_ids),
        "session_count": session_count,
        "noise_session_count": noise_session_count,
        "clusters": clusters,
    }


__all__ = [
    "REQUIRED_FIELDS",
    "OPTIONAL_FIELDS",
    "OUTPUT_FIELDS",
    "NOISE_CLUSTER_ID",
    "build_cluster_analytics",
]
