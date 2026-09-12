"""
D4.1 / D4.2 / D4.3 — Feature Validation

Validates the frozen 48-feature contract.

This module:
- validates exact feature count
- validates feature names
- validates feature order
- rejects duplicate feature names
- rejects missing/unexpected features
- validates numeric and finite values
- preserves the existing validation API
- does NOT own FROZEN_FEATURE_ORDER

The frozen feature order remains defined exclusively in:
    app.pipeline.feature_generation
"""


import math
from typing import Any, Dict, List, Sequence, Tuple


def _get_frozen_feature_order() -> List[str]:
    """
    Lazily retrieve the single source of truth for the
    frozen 48-feature order.

    The import is intentionally local to avoid a circular
    import during module initialization.
    """

    from app.pipeline.feature_generation import (
        FROZEN_FEATURE_ORDER,
    )

    return list(FROZEN_FEATURE_ORDER)


def _is_numeric_finite(value: Any) -> bool:
    """
    Return True only for numeric, finite, non-boolean values.
    """

    if isinstance(value, bool):
        return False

    if not isinstance(value, (int, float)):
        return False

    return math.isfinite(value)


def _validate_feature_names(
    feature_names: Sequence[str],
    expected_order: Sequence[str] | None = None,
) -> None:
    """
    Validate feature names, count, uniqueness, membership,
    and exact order.

    If expected_order is not provided, the frozen production
    order is loaded lazily from feature_generation.
    """

    if expected_order is None:
        expected_order = _get_frozen_feature_order()

    expected = list(expected_order)
    actual = list(feature_names)

    if len(actual) != len(expected):
        raise ValueError(
            f"Expected exactly {len(expected)} features, "
            f"got {len(actual)}"
        )

    if len(set(actual)) != len(actual):
        duplicates = sorted(
            {
                name
                for name in actual
                if actual.count(name) > 1
            }
        )

        raise ValueError(
            f"Duplicate feature names: {duplicates}"
        )

    missing = sorted(
        set(expected) - set(actual)
    )

    if missing:
        raise ValueError(
            f"Missing features: {missing}"
        )

    unexpected = sorted(
        set(actual) - set(expected)
    )

    if unexpected:
        raise ValueError(
            f"Unexpected features: {unexpected}"
        )

    if actual != expected:
        raise ValueError(
            "Feature order does not match "
            "FROZEN_FEATURE_ORDER"
        )


def validate_48_feature_vector(
    feature_vector: Sequence[Tuple[str, Any]],
) -> bool:
    """
    Validate an ordered 48-feature vector.

    The ordered sequence representation is important because
    it can explicitly represent duplicate feature names,
    unlike a dictionary.
    """

    if not isinstance(feature_vector, (list, tuple)):
        raise TypeError(
            "feature_vector must be a list or tuple"
        )

    feature_names = []

    for item in feature_vector:
        if not isinstance(item, (list, tuple)):
            raise TypeError(
                "Each feature vector item must be a "
                "(name, value) pair"
            )

        if len(item) != 2:
            raise ValueError(
                "Each feature vector item must contain "
                "exactly a feature name and value"
            )

        name, value = item

        if not isinstance(name, str):
            raise TypeError(
                "Feature names must be strings"
            )

        feature_names.append(name)

        if not _is_numeric_finite(value):
            raise ValueError(
                f"Feature '{name}' at index "
                f"{len(feature_names) - 1} "
                "must be numeric and finite"
            )

    _validate_feature_names(
        feature_names,
    )

    return True


def validate_48_features(
    features: Dict[str, Any],
    expected_order: Sequence[str],
) -> bool:
    """
    Validate a dictionary-based 48-feature vector.

    The caller supplies the expected feature order explicitly.
    This keeps feature_generation.py as the single owner of
    FROZEN_FEATURE_ORDER while preserving the existing API.
    """

    if not isinstance(features, dict):
        raise TypeError(
            "features must be a dictionary"
        )

    feature_names = list(features.keys())

    _validate_feature_names(
        feature_names,
        expected_order,
    )

    for index, name in enumerate(feature_names):
        value = features[name]

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"Feature '{name}' at index {index} "
                "must be numeric and finite"
            )

        if not math.isfinite(value):
            raise ValueError(
                f"Feature '{name}' at index {index} "
                "must be numeric and finite"
            )

    return True
