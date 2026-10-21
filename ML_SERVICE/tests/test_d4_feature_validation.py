"""
D4.1 — Feature Validation Tests
"""

import math

import pytest

from app.pipeline.feature_generation import (
    FROZEN_FEATURE_ORDER,
)

from app.pipeline.feature_validation import (
    validate_48_feature_vector,
    validate_48_features,
)


def _valid_vector():
    return [
        (name, float(index + 1))
        for index, name in enumerate(
            FROZEN_FEATURE_ORDER
        )
    ]


def _valid_dict():
    return {
        name: float(index + 1)
        for index, name in enumerate(
            FROZEN_FEATURE_ORDER
        )
    }


def test_accepts_exactly_48_features():
    vector = _valid_vector()

    assert validate_48_feature_vector(
        vector
    ) is True


def test_accepts_correct_names_and_order():
    vector = _valid_vector()

    assert [
        name
        for name, _ in vector
    ] == FROZEN_FEATURE_ORDER


def test_accepts_numeric_finite_values():
    vector = _valid_vector()

    assert validate_48_feature_vector(
        vector
    ) is True


def test_rejects_47_features():
    vector = _valid_vector()[:-1]

    with pytest.raises(
        ValueError,
        match="Expected exactly 48 features",
    ):
        validate_48_feature_vector(vector)


def test_rejects_49_features():
    vector = _valid_vector()

    vector.append(
        ("event_count_extra", 1.0)
    )

    with pytest.raises(
        ValueError,
        match="Expected exactly 48 features",
    ):
        validate_48_feature_vector(vector)


def test_rejects_missing_feature():
    vector = _valid_vector()

    vector = [
        item
        for item in vector
        if item[0] != "event_count"
    ]

    vector.append(
        ("wrong_feature", 1.0)
    )

    with pytest.raises(
        ValueError,
        match="Missing features",
    ):
        validate_48_feature_vector(vector)


def test_rejects_unexpected_feature():
    vector = _valid_vector()

    vector[0] = (
        "unexpected_feature",
        1.0,
    )

    with pytest.raises(
        ValueError,
        match="Missing features",
    ):
        validate_48_feature_vector(vector)


def test_rejects_duplicate_feature():
    vector = _valid_vector()

    vector[1] = (
        FROZEN_FEATURE_ORDER[0],
        2.0,
    )

    with pytest.raises(
        ValueError,
        match="Duplicate feature names",
    ):
        validate_48_feature_vector(vector)


def test_rejects_wrong_order():
    vector = _valid_vector()

    vector[0], vector[1] = (
        vector[1],
        vector[0],
    )

    with pytest.raises(
        ValueError,
        match="Feature order",
    ):
        validate_48_feature_vector(vector)


def test_rejects_nan():
    vector = _valid_vector()

    vector[0] = (
        vector[0][0],
        math.nan,
    )

    with pytest.raises(
        ValueError,
        match="numeric and finite",
    ):
        validate_48_feature_vector(vector)


def test_rejects_positive_inf():
    vector = _valid_vector()

    vector[0] = (
        vector[0][0],
        math.inf,
    )

    with pytest.raises(
        ValueError,
        match="numeric and finite",
    ):
        validate_48_feature_vector(vector)


def test_rejects_negative_inf():
    vector = _valid_vector()

    vector[0] = (
        vector[0][0],
        -math.inf,
    )

    with pytest.raises(
        ValueError,
        match="numeric and finite",
    ):
        validate_48_feature_vector(vector)


def test_rejects_non_numeric_string():
    vector = _valid_vector()

    vector[0] = (
        vector[0][0],
        "not-a-number",
    )

    with pytest.raises(
        ValueError,
        match="numeric and finite",
    ):
        validate_48_feature_vector(vector)


def test_rejects_boolean():
    vector = _valid_vector()

    vector[0] = (
        vector[0][0],
        True,
    )

    with pytest.raises(
        ValueError,
        match="numeric and finite",
    ):
        validate_48_feature_vector(vector)


def test_dict_validation_accepts_valid_features():
    features = _valid_dict()

    assert validate_48_features(
        features,
        FROZEN_FEATURE_ORDER,
    ) is True


def test_dict_validation_rejects_wrong_order():
    features = _valid_dict()

    items = list(features.items())

    items[0], items[1] = (
        items[1],
        items[0],
    )

    wrong_order = dict(items)

    with pytest.raises(
        ValueError,
        match="Feature order",
    ):
        validate_48_features(
            wrong_order,
            FROZEN_FEATURE_ORDER,
        )
