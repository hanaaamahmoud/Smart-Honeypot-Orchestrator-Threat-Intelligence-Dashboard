"""
GeoIP input contract tests.

These tests verify that GeoIP fields can be present or absent
without requiring a non-existing canonical adapter function.
"""

from app.pipeline.normalization import normalize_event


def _base_event(**overrides):
    """Build a minimal event for normalization."""
    event = {
        "source_ip": "8.8.8.8",
        "timestamp": "2026-01-01T12:00:00Z",
        "destination_ip": "10.0.0.5",
        "destination_port": 22,
        "protocol": "ssh",
    }

    event.update(overrides)
    return event


def test_event_without_geoip_is_accepted():
    """An event without GeoIP data remains processable."""
    event = _base_event()

    normalized = normalize_event(event)

    assert normalized is not None
    assert normalized["source_ip"] == "8.8.8.8"


def test_event_with_geoip_is_accepted():
    """An event containing GeoIP data remains processable."""
    event = _base_event(
        country="US",
        country_code="US",
        city="Mountain View",
        latitude=37.4056,
        longitude=-122.0775,
        asn=15169,
        asn_org="Google LLC",
    )

    normalized = normalize_event(event)

    assert normalized is not None
    assert normalized["source_ip"] == "8.8.8.8"


def test_partial_geoip_is_accepted():
    """Partial GeoIP enrichment must not invalidate the event."""
    event = _base_event(
        country="US",
        country_code="US",
    )

    normalized = normalize_event(event)

    assert normalized is not None
    assert normalized["source_ip"] == "8.8.8.8"


def test_missing_geoip_does_not_remove_source_ip():
    """source_ip must remain available when GeoIP is absent."""
    event = _base_event()

    normalized = normalize_event(event)

    assert normalized is not None
    assert normalized["source_ip"] == "8.8.8.8"

