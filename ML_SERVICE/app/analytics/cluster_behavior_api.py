"""API enrichment for frozen production cluster behavior mapping."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MAPPING_PATH = Path(
    "/app/models/frozen_production_reference/"
    "cluster_behavior_mapping.json"
)


def load_cluster_behavior_mapping() -> dict[int, dict[str, Any]]:
    with MAPPING_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    mapping: dict[int, dict[str, Any]] = {}

    for entry in payload["clusters"]:
        cluster_id = int(entry["cluster_id"])
        mapping[cluster_id] = entry

    expected_ids = {-1, *range(38)}

    if set(mapping) != expected_ids:
        raise ValueError(
            "Cluster behavior mapping must contain exactly "
            "-1 and clusters 0..37."
        )

    return mapping


def enrich_result_with_cluster_behavior(
    result: dict[str, Any],
    mapping: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    cluster_id = int(
        result["production_cluster_assignment"]
    )

    if cluster_id not in mapping:
        raise ValueError(
            f"No behavior mapping found for production "
            f"cluster {cluster_id}."
        )

    behavior = mapping[cluster_id]

    enriched = dict(result)

    enriched["cluster_type"] = behavior["cluster_type"]
    enriched["activity_profile"] = behavior["activity_profile"]
    enriched["attacker_behavior"] = behavior["attacker_behavior"]
    enriched["confidence"] = behavior["confidence"]
    enriched["evidence_features"] = behavior["evidence_features"]

    # Add attack name only when the mapping explicitly provides one.
    if "possible_attack_name" in behavior:
        enriched["possible_attack_name"] = (
            behavior["possible_attack_name"]
        )

    return enriched
