import math
import pytest

from app.pipeline.feature_generation import (
    FROZEN_FEATURE_ORDER,
)

from app.pipeline.feature_validation import (
    validate_48_features,
)


def _complete_features():
    return {
        name: float(index + 1)
        for index, name
        in enumerate(FROZEN_FEATURE_ORDER)
    }


def test_valid_48_features_pass():
    features = _complete_features()
    assert validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    ) is True


def test_exactly_48_required():
    features = _complete_features()
    features.pop("event_count")
    with pytest.raises(
        ValueError,
        match="exactly 48",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_missing_feature_rejected():
    features = _complete_features()
    features.pop("event_count")
    features["fake_feature"] = 100.0
    with pytest.raises(
        ValueError,
        match="Missing features",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_unexpected_feature_rejected():
    features = _complete_features()
    features["unexpected_feature"] = 100.0
    with pytest.raises(
        ValueError,
        match="exactly 48",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_order_is_strictly_validated():
    features = _complete_features()
    reversed_features = {
        name: features[name]
        for name in reversed(
            FROZEN_FEATURE_ORDER
        )
    }
    with pytest.raises(
        ValueError,
        match="order",
    ):
        validate_48_features(
            reversed_features,
            FROZEN_FEATURE_ORDER,
        )


def test_non_numeric_feature_rejected():
    features = _complete_features()
    features["event_count"] = "not-a-number"
    with pytest.raises(
        TypeError,
        match="must be numeric",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_nan_rejected():
    features = _complete_features()
    features["event_count"] = math.nan
    with pytest.raises(
        ValueError,
        match="finite",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_positive_infinity_rejected():
    features = _complete_features()
    features["event_count"] = math.inf
    with pytest.raises(
        ValueError,
        match="finite",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_negative_infinity_rejected():
    features = _complete_features()
    features["event_count"] = -math.inf
    with pytest.raises(
        ValueError,
        match="finite",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_boolean_rejected_as_numeric():
    features = _complete_features()
    features["event_count"] = True
    with pytest.raises(
        TypeError,
        match="must be numeric",
    ):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_input_is_not_mutated():
    features = _complete_features()
    original = dict(features)
    validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    )
    assert features == original
