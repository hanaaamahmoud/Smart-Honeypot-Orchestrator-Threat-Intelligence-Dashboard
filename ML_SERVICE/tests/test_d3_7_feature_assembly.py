import pytest

from app.pipeline.feature_generation import (
    FROZEN_FEATURE_ORDER,
    assemble_48_features,
)


def _complete_features():
    return {
        feature_name: index + 1
        for index, feature_name
        in enumerate(FROZEN_FEATURE_ORDER)
    }


def test_exactly_48_features():
    features = _complete_features()

    result = assemble_48_features(features)

    assert len(result) == 48


def test_exact_feature_names():
    features = _complete_features()

    result = assemble_48_features(features)

    assert set(result.keys()) == set(
        FROZEN_FEATURE_ORDER
    )


def test_exact_frozen_order():
    features = _complete_features()

    result = assemble_48_features(features)

    assert list(result.keys()) == (
        FROZEN_FEATURE_ORDER
    )


def test_values_follow_frozen_order():
    features = _complete_features()

    result = assemble_48_features(features)

    for index, feature_name in enumerate(
        FROZEN_FEATURE_ORDER
    ):
        assert result[feature_name] == float(index + 1)


def test_missing_feature_is_rejected():
    features = _complete_features()

    features.pop("event_count")

    with pytest.raises(
        ValueError,
        match="Missing features",
    ):
        assemble_48_features(features)


def test_extra_feature_is_rejected():
    features = _complete_features()

    features["unexpected_feature"] = 999

    with pytest.raises(
        ValueError,
        match="Unexpected features",
    ):
        assemble_48_features(features)


def test_all_outputs_are_numeric():
    features = _complete_features()

    result = assemble_48_features(features)

    assert all(
        isinstance(value, float)
        for value in result.values()
    )


def test_assembly_does_not_modify_input():
    features = _complete_features()

    original = dict(features)

    assemble_48_features(features)

    assert features == original
