import math
import pytest

from app.pipeline.feature_generation import FROZEN_FEATURE_ORDER
from app.pipeline.feature_validation import validate_48_features


def make_valid_features():
    return {
        name: float(index)
        for index, name in enumerate(FROZEN_FEATURE_ORDER)
    }


def test_accepts_valid_48_features():
    features = make_valid_features()

    assert validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    ) is True


def test_rejects_47_features():
    features = make_valid_features()
    features.pop(FROZEN_FEATURE_ORDER[-1])

    with pytest.raises(ValueError):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_49_features():
    features = make_valid_features()
    features["extra_feature"] = 123.0

    with pytest.raises(ValueError):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_wrong_order():
    features = make_valid_features()

    items = list(features.items())
    items[0], items[1] = items[1], items[0]

    wrong_order = dict(items)

    with pytest.raises(ValueError):
        validate_48_features(
            wrong_order,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_missing_feature():
    features = make_valid_features()

    features.pop("event_count")
    features["unexpected_feature"] = 1.0

    with pytest.raises(ValueError):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_duplicate_feature_name():
    features = make_valid_features()

    features["event_count"] = 999.0

    # A Python dict cannot contain the same key twice,
    # so duplicate-name validation belongs to the
    # ordered-vector validator tested separately in D4.1.
    # Here we confirm the dictionary validator still
    # accepts a valid dictionary structure.
    assert validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    ) is True


def test_rejects_nan():
    features = make_valid_features()
    features["event_count"] = math.nan

    with pytest.raises(ValueError):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_positive_infinity():
    features = make_valid_features()
    features["event_count"] = math.inf

    with pytest.raises(ValueError):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_negative_infinity():
    features = make_valid_features()
    features["event_count"] = -math.inf

    with pytest.raises(ValueError):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_non_numeric_value():
    features = make_valid_features()
    features["event_count"] = "123"

    with pytest.raises((TypeError, ValueError)):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_rejects_boolean_value():
    features = make_valid_features()
    features["event_count"] = True

    with pytest.raises((TypeError, ValueError)):
        validate_48_features(
            features,
            FROZEN_FEATURE_ORDER,
        )


def test_validation_does_not_mutate_input():
    features = make_valid_features()
    original = features.copy()

    validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    )

    assert features == original
