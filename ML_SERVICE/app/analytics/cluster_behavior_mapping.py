import json
from pathlib import Path


OUTPUT = Path(
    "/app/models/frozen_production_reference/cluster_behavior_mapping.json"
)


SESSIONS = {
    -1: 1676,
    0: 981,
    1: 246,
    2: 241,
    3: 372,
    4: 984,
    5: 697,
    6: 243,
    7: 464,
    8: 521,
    9: 301,
    10: 243,
    11: 927,
    12: 496,
    13: 341,
    14: 245,
    15: 43,
    16: 243,
    17: 230,
    18: 124,
    19: 184,
    20: 95,
    21: 460,
    22: 244,
    23: 55,
    24: 242,
    25: 65,
    26: 230,
    27: 39,
    28: 58,
    29: 33,
    30: 243,
    31: 52,
    32: 107,
    33: 36,
    34: 23,
    35: 31,
    36: 44,
    37: 21,
}


PROFILES = {
    -1: {
        "cluster_type": "Anomalous / Outlier Activity",
        "activity_profile": "Behavior outside the learned DBSCAN behavioral clusters",
        "attacker_behavior": "Behavior requiring investigation because it falls outside the learned reference clusters",
        "confidence": "HIGH",
        "evidence_features": [
            "inter_event_gap_mean_log1p",
            "latitude_mean",
            "event_density",
            "events_per_second",
            "command_density",
        ],
    },

    0: {
        "cluster_type": "Geo-temporal Authentication Activity",
        "activity_profile": "Authentication activity with distinctive temporal and geographic characteristics",
        "attacker_behavior": "Repeated authentication-oriented activity with distinctive time and source-location characteristics",
        "confidence": "MEDIUM",
        "evidence_features": [
            "dayofweek",
            "dayofmonth",
            "longitude",
            "auth_attempt_rate",
            "username_diversity",
        ],
    },

    1: {
        "cluster_type": "Authentication-focused Activity",
        "activity_profile": "High authentication-attempt activity with multiple usernames",
        "attacker_behavior": "Credential / Authentication Attack Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Credential / Authentication Attack",
        "evidence_features": [
            "auth_attempt_rate",
            "username_diversity",
            "unique_usernames",
            "latitude",
            "geo_longitude_abs",
        ],
    },

    2: {
        "cluster_type": "Geo-temporal Activity",
        "activity_profile": "Geographically distinctive activity with username variation",
        "attacker_behavior": "Repeated activity from a distinctive geographic and temporal pattern",
        "confidence": "MEDIUM",
        "evidence_features": [
            "longitude",
            "username_diversity",
            "unique_usernames",
            "latitude",
            "hour",
        ],
    },

    3: {
        "cluster_type": "Multi-target / Multi-protocol Activity",
        "activity_profile": "High diversity across destinations, protocols, honeypots and ports",
        "attacker_behavior": "Reconnaissance-like Activity",
        "confidence": "MEDIUM",
        "possible_attack_name": "Reconnaissance-like Activity",
        "evidence_features": [
            "unique_destinations",
            "protocol_diversity",
            "honeypot_diversity",
            "destination_port_diversity",
            "geo_country_diversity",
        ],
    },

    4: {
        "cluster_type": "Geo-temporal Activity",
        "activity_profile": "Geographically and temporally distinctive activity",
        "attacker_behavior": "Repeated activity associated with a distinctive source-location and time pattern",
        "confidence": "MEDIUM",
        "evidence_features": [
            "geo_longitude_abs",
            "longitude",
            "hour",
            "unique_usernames",
            "username_diversity",
        ],
    },

    5: {
        "cluster_type": "Geo-temporal Activity",
        "activity_profile": "Activity concentrated around specific calendar and geographic characteristics",
        "attacker_behavior": "Repeated activity with distinctive temporal and source-location characteristics",
        "confidence": "MEDIUM",
        "evidence_features": [
            "dayofweek",
            "geo_longitude_abs",
            "longitude",
            "dayofmonth",
            "username_diversity",
        ],
    },

    6: {
        "cluster_type": "Authentication-focused Activity",
        "activity_profile": "High authentication rate with geographic and username concentration",
        "attacker_behavior": "Credential / Authentication Attack Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Credential / Authentication Attack",
        "evidence_features": [
            "auth_attempt_rate",
            "session_hour",
            "latitude",
            "geo_latitude_abs",
            "username_diversity",
        ],
    },

    7: {
        "cluster_type": "Geo-temporal Authentication Activity",
        "activity_profile": "Authentication-oriented activity with distinctive longitude and username characteristics",
        "attacker_behavior": "Authentication Activity Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Authentication Activity",
        "evidence_features": [
            "geo_longitude_abs",
            "longitude",
            "username_diversity",
            "auth_attempt_rate",
            "unique_usernames",
        ],
    },

    8: {
        "cluster_type": "Time-concentrated Activity",
        "activity_profile": "Activity concentrated around specific session hours with username variation",
        "attacker_behavior": "Time-concentrated repeated activity",
        "confidence": "MEDIUM",
        "evidence_features": [
            "session_hour",
            "username_diversity",
            "unique_usernames",
        ],
    },

    9: {
        "cluster_type": "Long-duration Sparse Activity",
        "activity_profile": "Longer-duration activity with large inter-event gaps",
        "attacker_behavior": "Sparse and persistent activity over extended periods",
        "confidence": "MEDIUM",
        "evidence_features": [
            "geo_latitude_abs",
            "latitude",
            "duration",
            "max_inter_event_gap",
            "inter_event_gap_mean",
        ],
    },

    10: {
        "cluster_type": "Geo-temporal Authentication Activity",
        "activity_profile": "Authentication activity with strong latitude and calendar characteristics",
        "attacker_behavior": "Authentication Activity Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Authentication Activity",
        "evidence_features": [
            "geo_latitude_abs",
            "dayofweek",
            "latitude",
            "auth_attempt_rate",
            "dayofmonth",
        ],
    },

    11: {
        "cluster_type": "Geo-temporal Activity",
        "activity_profile": "Longitude and username-focused activity with reduced protocol diversity",
        "attacker_behavior": "Repeated activity with distinctive geographic and username characteristics",
        "confidence": "MEDIUM",
        "evidence_features": [
            "geo_longitude_abs",
            "longitude",
            "username_diversity",
            "unique_usernames",
        ],
    },

    12: {
        "cluster_type": "Multi-target / Multi-protocol Activity",
        "activity_profile": "High diversity across destinations, protocols, honeypots and ports",
        "attacker_behavior": "Reconnaissance-like Activity",
        "confidence": "MEDIUM",
        "possible_attack_name": "Reconnaissance-like Activity",
        "evidence_features": [
            "unique_destinations",
            "protocol_diversity",
            "honeypot_diversity",
            "destination_port_diversity",
            "geo_country_diversity",
        ],
    },

    13: {
        "cluster_type": "Multi-target / Multi-protocol Activity",
        "activity_profile": "Multi-target and multi-protocol behavior with geographic diversity",
        "attacker_behavior": "Reconnaissance-like Activity",
        "confidence": "MEDIUM",
        "possible_attack_name": "Reconnaissance-like Activity",
        "evidence_features": [
            "unique_destinations",
            "protocol_diversity",
            "honeypot_diversity",
            "destination_port_diversity",
            "geo_country_diversity",
        ],
    },

    14: {
        "cluster_type": "Geo-temporal Authentication Activity",
        "activity_profile": "Authentication-oriented activity with strong latitude and username characteristics",
        "attacker_behavior": "Authentication Activity Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Authentication Activity",
        "evidence_features": [
            "geo_latitude_abs",
            "latitude",
            "auth_attempt_rate",
            "username_diversity",
            "unique_usernames",
        ],
    },

    15: {
        "cluster_type": "Username-focused Activity",
        "activity_profile": "Strong username and unique-username characteristics",
        "attacker_behavior": "Credential Activity Candidate",
        "confidence": "LOW",
        "possible_attack_name": "Credential Activity",
        "evidence_features": [
            "username_diversity",
            "unique_usernames",
        ],
    },

    16: {
        "cluster_type": "Geo-temporal Activity",
        "activity_profile": "Geographically distinctive activity with username variation",
        "attacker_behavior": "Repeated source-location activity with limited protocol diversity",
        "confidence": "MEDIUM",
        "evidence_features": [
            "longitude",
            "latitude",
            "username_diversity",
            "geo_longitude_abs",
            "unique_usernames",
        ],
    },

    17: {
        "cluster_type": "Time-concentrated Activity",
        "activity_profile": "Activity concentrated around specific hours with username variation",
        "attacker_behavior": "Time-concentrated repeated activity",
        "confidence": "MEDIUM",
        "evidence_features": [
            "hour",
            "longitude",
            "username_diversity",
            "unique_usernames",
        ],
    },

    18: {
        "cluster_type": "Multi-target / Multi-protocol Activity",
        "activity_profile": "High diversity across destinations, protocols, honeypots and ports",
        "attacker_behavior": "Reconnaissance-like Activity",
        "confidence": "MEDIUM",
        "possible_attack_name": "Reconnaissance-like Activity",
        "evidence_features": [
            "unique_destinations",
            "protocol_diversity",
            "honeypot_diversity",
            "destination_port_diversity",
            "geo_country_diversity",
        ],
    },

    19: {
        "cluster_type": "Geo-temporal Activity",
        "activity_profile": "Latitude and hour focused activity with username variation",
        "attacker_behavior": "Repeated activity with distinctive geographic and temporal characteristics",
        "confidence": "MEDIUM",
        "evidence_features": [
            "hour",
            "latitude",
            "geo_latitude_abs",
            "username_diversity",
            "unique_usernames",
        ],
    },

    20: {
        "cluster_type": "Long-duration Sparse Activity",
        "activity_profile": "Long-duration activity with large temporal gaps",
        "attacker_behavior": "Sparse and persistent activity over extended periods",
        "confidence": "MEDIUM",
        "evidence_features": [
            "geo_longitude_abs",
            "hour",
            "longitude",
            "duration",
            "max_inter_event_gap",
        ],
    },

    21: {
        "cluster_type": "Geo-temporal Activity",
        "activity_profile": "Longitude and username-focused activity with limited protocol diversity",
        "attacker_behavior": "Repeated activity with distinctive geographic characteristics",
        "confidence": "MEDIUM",
        "evidence_features": [
            "geo_longitude_abs",
            "longitude",
            "hour",
            "username_diversity",
            "unique_usernames",
        ],
    },

    22: {
        "cluster_type": "Low-diversity Authentication Activity",
        "activity_profile": "Authentication activity with username concentration and limited diversity",
        "attacker_behavior": "Authentication Activity Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Authentication Activity",
        "evidence_features": [
            "username_diversity",
            "unique_usernames",
            "auth_attempt_rate",
        ],
    },

    23: {
        "cluster_type": "Time-concentrated Username Activity",
        "activity_profile": "Username-focused activity concentrated around specific hours",
        "attacker_behavior": "Credential Activity Candidate",
        "confidence": "LOW",
        "possible_attack_name": "Credential Activity",
        "evidence_features": [
            "hour",
            "username_diversity",
            "unique_usernames",
        ],
    },

    24: {
        "cluster_type": "Authentication-focused Activity",
        "activity_profile": "High authentication rate with geographic and temporal concentration",
        "attacker_behavior": "Credential / Authentication Attack Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Credential / Authentication Attack",
        "evidence_features": [
            "auth_attempt_rate",
            "latitude",
            "hour",
            "geo_latitude_abs",
            "username_diversity",
        ],
    },

    25: {
        "cluster_type": "Geo-temporal Username Activity",
        "activity_profile": "Username-focused activity with distinctive longitude characteristics",
        "attacker_behavior": "Repeated username-oriented activity with limited protocol diversity",
        "confidence": "MEDIUM",
        "evidence_features": [
            "longitude",
            "username_diversity",
            "unique_usernames",
        ],
    },

    26: {
        "cluster_type": "Username-focused Activity",
        "activity_profile": "Strong username and unique-username characteristics",
        "attacker_behavior": "Credential Activity Candidate",
        "confidence": "LOW",
        "possible_attack_name": "Credential Activity",
        "evidence_features": [
            "username_diversity",
            "unique_usernames",
        ],
    },

    27: {
        "cluster_type": "Authentication-focused Activity",
        "activity_profile": "High authentication rate with geographic and temporal concentration",
        "attacker_behavior": "Credential / Authentication Attack Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Credential / Authentication Attack",
        "evidence_features": [
            "auth_attempt_rate",
            "latitude",
            "geo_latitude_abs",
            "hour",
            "username_diversity",
        ],
    },

    28: {
        "cluster_type": "Geo-temporal Username Activity",
        "activity_profile": "Username-oriented activity with calendar and longitude characteristics",
        "attacker_behavior": "Repeated username-oriented activity with distinctive timing and source location",
        "confidence": "MEDIUM",
        "evidence_features": [
            "dayofweek",
            "dayofmonth",
            "longitude",
            "username_diversity",
        ],
    },

    29: {
        "cluster_type": "Authentication-focused Activity",
        "activity_profile": "Authentication activity concentrated around specific hours and usernames",
        "attacker_behavior": "Credential / Authentication Attack Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Credential / Authentication Attack",
        "evidence_features": [
            "auth_attempt_rate",
            "hour",
            "latitude",
            "username_diversity",
        ],
    },

    30: {
        "cluster_type": "Geo-temporal Authentication Activity",
        "activity_profile": "Authentication-oriented activity with strong latitude and username characteristics",
        "attacker_behavior": "Authentication Activity Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Authentication Activity",
        "evidence_features": [
            "geo_latitude_abs",
            "latitude",
            "username_diversity",
            "auth_attempt_rate",
            "unique_usernames",
        ],
    },

    31: {
        "cluster_type": "Geo-temporal Username Activity",
        "activity_profile": "Username-oriented activity with distinctive calendar characteristics",
        "attacker_behavior": "Repeated username-oriented activity with distinctive timing",
        "confidence": "MEDIUM",
        "evidence_features": [
            "dayofweek",
            "dayofmonth",
            "username_diversity",
        ],
    },

    32: {
        "cluster_type": "Geo-temporal Username Activity",
        "activity_profile": "Time and longitude-focused activity with username variation",
        "attacker_behavior": "Repeated activity with distinctive temporal and geographic characteristics",
        "confidence": "MEDIUM",
        "evidence_features": [
            "hour",
            "longitude",
            "username_diversity",
            "unique_usernames",
            "latitude",
        ],
    },

    33: {
        "cluster_type": "Authentication-focused Activity",
        "activity_profile": "Authentication activity with strong latitude and username characteristics",
        "attacker_behavior": "Authentication Activity Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Authentication Activity",
        "evidence_features": [
            "latitude",
            "geo_latitude_abs",
            "auth_attempt_rate",
            "username_diversity",
        ],
    },

    34: {
        "cluster_type": "Low-credential Activity",
        "activity_profile": "Activity with low username diversity and low authentication characteristics",
        "attacker_behavior": "Low-diversity activity without sufficient evidence for a specific attack label",
        "confidence": "LOW",
        "evidence_features": [
            "dayofweek",
            "username_diversity",
            "unique_usernames",
            "auth_attempt_rate",
            "credential_attempt_density",
        ],
    },

    35: {
        "cluster_type": "Authentication-focused Activity",
        "activity_profile": "Authentication activity with strong latitude and username characteristics",
        "attacker_behavior": "Credential / Authentication Attack Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Credential / Authentication Attack",
        "evidence_features": [
            "auth_attempt_rate",
            "latitude",
            "username_diversity",
            "unique_usernames",
        ],
    },

    36: {
        "cluster_type": "Multi-target / Multi-protocol Activity",
        "activity_profile": "High diversity across destinations, honeypots, protocols and ports",
        "attacker_behavior": "Reconnaissance-like Activity",
        "confidence": "MEDIUM",
        "possible_attack_name": "Reconnaissance-like Activity",
        "evidence_features": [
            "unique_destinations",
            "honeypot_diversity",
            "protocol_diversity",
            "destination_port_diversity",
            "geo_country_diversity",
        ],
    },

    37: {
        "cluster_type": "Sparse Long-duration Multi-target Activity",
        "activity_profile": "Long-duration sparse activity combined with multi-target and multi-protocol diversity",
        "attacker_behavior": "Reconnaissance-like / Slow Exploration Candidate",
        "confidence": "MEDIUM",
        "possible_attack_name": "Reconnaissance-like / Slow Exploration",
        "evidence_features": [
            "inter_event_gap_mean_log1p",
            "max_inter_event_gap",
            "duration",
            "protocol_diversity",
            "honeypot_diversity",
            "destination_port_diversity",
            "unique_destinations",
            "geo_country_diversity",
        ],
    },
}


def build_cluster_entry(cluster_id):
    profile = PROFILES[cluster_id]

    entry = {
        "cluster_id": cluster_id,
        "session_count": SESSIONS[cluster_id],
        "cluster_type": profile["cluster_type"],
        "activity_profile": profile["activity_profile"],
        "attacker_behavior": profile["attacker_behavior"],
        "confidence": profile["confidence"],
        "evidence_features": profile["evidence_features"],
        "evidence_source": "Step 7D DBSCAN behavioral reference",
        "mapping_status": "INTERPRETATION_LAYER_ONLY",
    }

    if "possible_attack_name" in profile:
        entry["possible_attack_name"] = profile["possible_attack_name"]

    return entry


def validate(entries):
    expected_ids = set(range(0, 38))
    expected_ids.add(-1)

    actual_ids = {entry["cluster_id"] for entry in entries}

    assert len(entries) == 39, f"Expected 39 entries, got {len(entries)}"
    assert actual_ids == expected_ids, (
        f"Cluster IDs mismatch. Expected {sorted(expected_ids)}, "
        f"got {sorted(actual_ids)}"
    )

    required_fields = {
        "cluster_id",
        "session_count",
        "cluster_type",
        "activity_profile",
        "attacker_behavior",
        "confidence",
        "evidence_features",
        "evidence_source",
        "mapping_status",
    }

    for entry in entries:
        missing = required_fields - set(entry.keys())
        assert not missing, (
            f"Cluster {entry['cluster_id']} missing fields: {sorted(missing)}"
        )

        assert entry["cluster_type"]
        assert entry["activity_profile"]
        assert entry["attacker_behavior"]
        assert entry["confidence"]
        assert entry["evidence_features"]
        assert entry["evidence_source"]
        assert entry["mapping_status"]

        for key, value in entry.items():
            assert value is not None, (
                f"Cluster {entry['cluster_id']} contains null value in {key}"
            )

        if "possible_attack_name" in entry:
            assert entry["possible_attack_name"].strip()

    return True


def main():
    entries = [
        build_cluster_entry(cluster_id)
        for cluster_id in sorted(PROFILES.keys())
    ]

    validate(entries)

    named = [
        entry
        for entry in entries
        if "possible_attack_name" in entry
    ]

    activity_only = [
        entry
        for entry in entries
        if "possible_attack_name" not in entry
    ]

    payload = {
        "mapping_version": "1.0",
        "mapping_type": "FROZEN_CLUSTER_BEHAVIOR_INTERPRETATION",
        "model_status": "FROZEN_PRODUCTION_REFERENCE",
        "source": "Step 7D DBSCAN behavioral reference",
        "cluster_count": 38,
        "noise_included": True,
        "total_entries": len(entries),
        "attack_name_policy": (
            "possible_attack_name is emitted only when the available "
            "behavioral evidence supports a useful candidate label"
        ),
        "entries": entries,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as handle:
        json.dump(
            payload,
            handle,
            indent=2,
            ensure_ascii=False,
        )

    print("CLUSTER BEHAVIOR MAPPING: PASS")
    print(f"total entries: {len(entries)}")
    print(f"named activity entries: {len(named)}")
    print(f"activity-only entries: {len(activity_only)}")
    print("cluster IDs: -1, 0..37")
    print(f"output: {OUTPUT}")


if __name__ == "__main__":
    main()
