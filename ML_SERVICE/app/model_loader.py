"""
Frozen production ML artifact loader.

IMPORTANT:
- Read-only artifacts only.
- No DBSCAN fitting.
- No retraining.
- No new cluster creation.
- Future assignment uses nearest frozen behavioral centroid.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


MODEL_DIR = Path("/app/models")
REFERENCE_DIR = MODEL_DIR / "frozen_production_reference"

SHA256_FILE = MODEL_DIR / "frozen_reference_sha256.json"
SCALER_FILE = REFERENCE_DIR / "standard_scaler_params.json"
FEATURE_SCHEMA_FILE = REFERENCE_DIR / "step7h_production_feature_schema.json"
CONFIG_FILE = REFERENCE_DIR / "step7g_production_config.json"
BEHAVIORAL_REFERENCE_FILE = (
    REFERENCE_DIR / "step7d_behavioral_reference.json"
)
CENTROIDS_FILE = (
    REFERENCE_DIR / "step7g_dbscan_behavioral_reference_centroids.csv"
)


class FrozenModelError(RuntimeError):
    """Raised when frozen production artifacts are invalid."""


class FrozenModel:
    """
    Read-only frozen production model.

    This object does not fit DBSCAN.

    It only:
    1. validates the 48-feature contract,
    2. applies the frozen StandardScaler parameters,
    3. finds the nearest frozen behavioral centroid.
    """

    def __init__(
        self,
        feature_names,
        scaler_mean,
        scaler_scale,
        centroids,
        config,
    ):
        self.feature_names = tuple(feature_names)
        self.scaler_mean = tuple(scaler_mean)
        self.scaler_scale = tuple(scaler_scale)
        self.centroids = tuple(centroids)
        self.config = dict(config)

        self.feature_count = len(self.feature_names)

    def scale_features(self, features: dict[str, float]) -> list[float]:
        """
        Apply the frozen StandardScaler parameters.
        """

        if list(features.keys()) != list(self.feature_names):
            raise FrozenModelError(
                "Feature names/order do not match frozen production contract."
            )

        values = []

        for index, name in enumerate(self.feature_names):
            value = float(features[name])

            scale = float(self.scaler_scale[index])

            safe_scale = scale if scale != 0.0 else 1.0

            scaled_value = (
                value - float(self.scaler_mean[index])
            ) / safe_scale

            values.append(scaled_value)

        return values

    def nearest_centroid(
        self,
        scaled_features: list[float],
    ) -> tuple[int, float]:
        """
        Find the nearest frozen behavioral centroid
        using Euclidean distance.
        """

        if len(scaled_features) != self.feature_count:
            raise FrozenModelError(
                f"Expected {self.feature_count} scaled features, "
                f"got {len(scaled_features)}."
            )

        best_cluster = None
        best_distance = None

        for centroid in self.centroids:
            cluster_id = int(centroid["dbscan_cluster"])
            vector = centroid["vector"]

            distance_squared = sum(
                (
                    float(x) - float(y)
                ) ** 2
                for x, y in zip(
                    scaled_features,
                    vector,
                )
            )

            distance = distance_squared ** 0.5

            if (
                best_distance is None
                or distance < best_distance
            ):
                best_distance = distance
                best_cluster = cluster_id

        if best_cluster is None or best_distance is None:
            raise FrozenModelError(
                "No frozen behavioral centroids are available."
            )

        return best_cluster, best_distance


def _sha256(path: Path) -> str:
    """
    Calculate SHA-256 for a file.
    """

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def _load_json(path: Path) -> dict:
    """
    Load a JSON object.
    """

    if not path.exists():
        raise FrozenModelError(
            f"Required frozen artifact does not exist: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as handle:
            return json.load(handle)

    except Exception as exc:
        raise FrozenModelError(
            f"Could not load JSON artifact: {path}"
        ) from exc


def _verify_sha256() -> None:
    """
    Verify all frozen production artifacts against
    the immutable SHA-256 manifest.
    """

    manifest = _load_json(SHA256_FILE)

    if not isinstance(manifest, dict):
        raise FrozenModelError(
            "Frozen SHA-256 manifest must be a JSON object."
        )

    for filename, expected_hash in manifest.items():

        path = REFERENCE_DIR / filename

        if not path.exists():
            raise FrozenModelError(
                "Frozen artifact listed in SHA-256 manifest "
                f"is missing: {filename}"
            )

        actual_hash = _sha256(path)

        if actual_hash != expected_hash:
            raise FrozenModelError(
                f"SHA-256 mismatch for frozen artifact: {filename}"
            )


def _validate_feature_contract(
    config: dict,
    behavioral_reference: dict,
    feature_schema: dict,
) -> list[str]:
    """
    Validate that all production artifacts use exactly
    the same 48 behavioral features and ordering.
    """

    config_features = config.get("behavioral_features")

    reference_features = behavioral_reference.get(
        "behavioral_features"
    )

    schema_features = feature_schema.get(
        "behavioral_features"
    )

    if config_features != reference_features:
        raise FrozenModelError(
            "Config and behavioral reference feature contracts differ."
        )

    if config_features != schema_features:
        raise FrozenModelError(
            "Config and feature schema contracts differ."
        )

    if not isinstance(config_features, list):
        raise FrozenModelError(
            "Behavioral feature contract must be a list."
        )

    if len(config_features) != 48:
        raise FrozenModelError(
            "Frozen production feature contract must contain "
            "exactly 48 features."
        )

    if len(set(config_features)) != 48:
        raise FrozenModelError(
            "Frozen production feature contract contains duplicates."
        )

    return list(config_features)


def _load_scaler(
    feature_names: list[str],
) -> tuple[list[float], list[float]]:
    """
    Load the primary frozen production StandardScaler.

    The primary artifact stores mean and scale as
    dictionaries keyed by feature name.
    """

    scaler = _load_json(SCALER_FILE)

    if scaler.get("feature_count") != 48:
        raise FrozenModelError(
            "Frozen scaler feature_count must be 48."
        )

    scaler_features = scaler.get("features")

    if scaler_features != feature_names:
        raise FrozenModelError(
            "Frozen scaler feature order does not match "
            "the production feature contract."
        )

    mean = scaler.get("mean")
    scale = scaler.get("scale")

    if not isinstance(mean, dict) or not isinstance(scale, dict):
        raise FrozenModelError(
            "Frozen scaler mean/scale must be "
            "feature-name mappings."
        )

    if set(mean.keys()) != set(feature_names):
        raise FrozenModelError(
            "Frozen scaler mean keys do not match "
            "feature contract."
        )

    if set(scale.keys()) != set(feature_names):
        raise FrozenModelError(
            "Frozen scaler scale keys do not match "
            "feature contract."
        )

    try:
        mean_values = [
            float(mean[name])
            for name in feature_names
        ]

        scale_values = [
            float(scale[name])
            for name in feature_names
        ]

    except Exception as exc:
        raise FrozenModelError(
            "Frozen scaler contains non-numeric "
            "mean/scale values."
        ) from exc

    if len(mean_values) != 48:
        raise FrozenModelError(
            "Frozen scaler mean must contain 48 values."
        )

    if len(scale_values) != 48:
        raise FrozenModelError(
            "Frozen scaler scale must contain 48 values."
        )

    return mean_values, scale_values


def _load_centroids(
    feature_names: list[str],
) -> list[dict]:
    """
    Load the frozen behavioral centroid table.

    Centroid values are already in standardized
    feature space.
    """

    if not CENTROIDS_FILE.exists():
        raise FrozenModelError(
            "Frozen centroid artifact does not exist: "
            f"{CENTROIDS_FILE}"
        )

    expected_columns = [
        "dbscan_cluster",
        "session_count",
        *feature_names,
    ]

    centroids = []

    with CENTROIDS_FILE.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:

        reader = csv.DictReader(handle)

        if reader.fieldnames != expected_columns:
            raise FrozenModelError(
                "Frozen centroid CSV columns do not match "
                "the 48-feature production contract."
            )

        for row in reader:

            try:
                cluster_id = int(
                    row["dbscan_cluster"]
                )

                session_count = int(
                    row["session_count"]
                )

                vector = [
                    float(row[name])
                    for name in feature_names
                ]

            except Exception as exc:
                raise FrozenModelError(
                    "Frozen centroid CSV contains "
                    "invalid numeric values."
                ) from exc

            if len(vector) != 48:
                raise FrozenModelError(
                    "Frozen centroid does not contain "
                    "48 features."
                )

            centroids.append(
                {
                    "dbscan_cluster": cluster_id,
                    "session_count": session_count,
                    "vector": vector,
                }
            )

    if len(centroids) != 38:
        raise FrozenModelError(
            "Expected exactly 38 frozen non-noise "
            f"centroids, got {len(centroids)}."
        )

    cluster_ids = sorted(
        item["dbscan_cluster"]
        for item in centroids
    )

    expected_cluster_ids = list(range(38))

    if cluster_ids != expected_cluster_ids:
        raise FrozenModelError(
            "Frozen centroid cluster IDs do not match "
            "expected reference clusters 0..37."
        )

    return centroids


def load_frozen_model() -> FrozenModel:
    """
    Load and validate the complete frozen production model.
    """

    # Verify all immutable production artifacts.
    _verify_sha256()

    # Load production configuration artifacts.
    config = _load_json(CONFIG_FILE)

    behavioral_reference = _load_json(
        BEHAVIORAL_REFERENCE_FILE
    )

    feature_schema = _load_json(
        FEATURE_SCHEMA_FILE
    )

    # Validate production model identity.
    if config.get("primary_model") != "DBSCAN":
        raise FrozenModelError(
            "Frozen production primary model is not DBSCAN."
        )

    if config.get("assignment_method_for_future_logs") != (
        "nearest_behavioral_centroid"
    ):
        raise FrozenModelError(
            "Frozen production assignment method is invalid."
        )

    if config.get("noise_label") != -1:
        raise FrozenModelError(
            "Frozen production noise label must be -1."
        )

    if config.get("reference_non_noise_clusters") != 38:
        raise FrozenModelError(
            "Frozen production reference must contain "
            "38 non-noise clusters."
        )

    # Validate exact 48-feature contract.
    feature_names = _validate_feature_contract(
        config,
        behavioral_reference,
        feature_schema,
    )

    # Load frozen scaler.
    scaler_mean, scaler_scale = _load_scaler(
        feature_names
    )

    # Load frozen behavioral centroids.
    centroids = _load_centroids(
        feature_names
    )

    # Return read-only in-memory model representation.
    return FrozenModel(
        feature_names=feature_names,
        scaler_mean=scaler_mean,
        scaler_scale=scaler_scale,
        centroids=centroids,
        config=config,
    )
