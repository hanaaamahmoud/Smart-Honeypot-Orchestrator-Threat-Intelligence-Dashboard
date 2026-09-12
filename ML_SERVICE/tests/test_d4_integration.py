"""
D4.3 — Integration Validation Tests

Verifies that the final 48-feature output produced by
D3 assembly satisfies the D4 validation contract.
"""

import math

import pytest

from app.pipeline.feature_generation import (
    FROZEN_FEATURE_ORDER,
    assemble_48_features,
)

from app.pipeline.feature_validation import (
    validate_48_features,
)


def _valid_feature_groups():
    return {
        name: float(index + 1)
        for index, name in enumerate(
            FROZEN_FEATURE_ORDER
        )
    }


def test_assembled_features_pass_validation():
    feature_groups = _valid_feature_groups()

    features = assemble_48_features(
        feature_groups
    )

    assert validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    ) is True


def test_assembled_features_have_exactly_48_features():
    feature_groups = _valid_feature_groups()

    features = assemble_48_features(
        feature_groups
    )

    assert len(features) == 48


def test_assembled_features_preserve_frozen_order():
    feature_groups = _valid_feature_groups()

    features = assemble_48_features(
        feature_groups
    )

    assert list(features.keys()) == (
        FROZEN_FEATURE_ORDER
    )


def test_assembled_features_are_numeric_and_finite():
    feature_groups = _valid_feature_groups()

    features = assemble_48_features(
        feature_groups
    )

    assert validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    ) is True

    for value in features.values():
        assert isinstance(value, float)
        assert math.isfinite(value)


def test_assembly_rejects_missing_feature():
    feature_groups = _valid_feature_groups()

    feature_groups.pop(
        FROZEN_FEATURE_ORDER[-1]
    )

    with pytest.raises(ValueError):
        assemble_48_features(
            feature_groups
        )


def test_assembly_rejects_unexpected_feature():
    feature_groups = _valid_feature_groups()

    feature_groups["unexpected_feature"] = 1.0

    with pytest.raises(ValueError):
        assemble_48_features(
            feature_groups
        )


def test_assembly_and_validation_are_consistent():
    feature_groups = _valid_feature_groups()

    features = assemble_48_features(
        feature_groups
    )

    assert list(features.keys()) == (
        FROZEN_FEATURE_ORDER
    )

    assert validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    ) is True
