"""
Production assignment layer.

This module is inference-only.

The production object supplied to this module must already be
prepared before runtime. This layer does not alter that object
and does not create behavioral groups.
"""

from __future__ import annotations

from typing import Any, Sequence


EXPECTED_FEATURE_COUNT = 48


class FrozenAssignmentError(RuntimeError):
    """Raised when production assignment cannot be completed."""


def validate_feature_vector(
    features: Sequence[float],
) -> list[float]:
    """
    Validate one production feature vector.

    The frozen production contract requires exactly 48 values.
    """

    if features is None:
        raise FrozenAssignmentError(
            "Feature vector is None."
        )

    values = list(features)

    if len(values) != EXPECTED_FEATURE_COUNT:
        raise FrozenAssignmentError(
            f"Expected {EXPECTED_FEATURE_COUNT} features, "
            f"received {len(values)}."
        )

    return values


def assign_with_frozen_model(
    model: Any,
    features: Sequence[float],
) -> Any:
    """
    Perform inference with the supplied frozen production object.

    No model preparation or state mutation occurs here.
    """

    values = validate_feature_vector(features)

    if model is None:
        raise FrozenAssignmentError(
            "Frozen production object was not supplied."
        )

    if hasattr(model, "predict"):
        predictor = getattr(
            model,
            "predict",
        )

        return predictor([values])

    if hasattr(model, "assign"):
        assigner = getattr(
            model,
            "assign",
        )

        return assigner(values)

    raise FrozenAssignmentError(
        "Frozen production object does not expose "
        "a supported inference interface."
    )


def normalize_assignment_result(
    result: Any,
) -> Any:
    """
    Normalize a single returned assignment value.
    """

    if isinstance(result, (list, tuple)):

        if len(result) == 1:
            return result[0]

    try:

        shape = getattr(
            result,
            "shape",
            None,
        )

        if shape == (1,):
            return result[0]

    except Exception:
        pass

    return result


__all__ = [
    "EXPECTED_FEATURE_COUNT",
    "FrozenAssignmentError",
    "validate_feature_vector",
    "assign_with_frozen_model",
    "normalize_assignment_result",
]
