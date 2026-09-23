"""Session analytics adapter for validated Step 9F assignment output."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable


REQUIRED_FIELDS = (
    "reconstructed_session_id",
    "production_cluster_assignment",
    "assignment_status",
    "feature_validation_status",
)

OPTIONAL_FIELDS = (
    "event_count",
    "session_start",
    "session_end",
    "source",
)

ALLOWED_CLUSTER_VALUES = {
    "EXISTING_PRODUCTION_CLUSTER",
    "NOISE",
}

OUTPUT_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS


def _validate_record(record: dict[str, Any]) -> None:
    missing = [
        field for field in REQUIRED_FIELDS
        if field not in record
    ]

    if missing:
        raise ValueError(
            f"Missing required session analytics fields: {missing}"
        )

    null_required = [
        field for field in REQUIRED_FIELDS
        if record[field] is None
    ]

    if null_required:
        raise ValueError(
            "Required session analytics fields cannot be null: "
            f"{null_required}"
        )

    if record["production_cluster_assignment"] not in ALLOWED_CLUSTER_VALUES:
        raise ValueError(
            "production_cluster_assignment must be one of "
            f"{sorted(ALLOWED_CLUSTER_VALUES)}"
        )


def build_session_analytics(
    results: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Validate and expose one analytics row for each validated input session.

    This adapter does not assign clusters, create clusters, retrain the model,
    or fabricate missing session metadata.
    """

    output: list[dict[str, Any]] = []

    for record in results:
        if not isinstance(record, dict):
            raise TypeError(
                "Each session analytics input must be a dictionary"
            )

        _validate_record(record)

        row = {
            field: deepcopy(record[field])
            for field in OUTPUT_FIELDS
            if field in record
        }

        output.append(row)

    return output
