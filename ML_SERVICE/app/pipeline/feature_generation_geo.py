"""
D3.6 — Geo / Availability Feature Generation

Generates:
- latitude_mean
- longitude_mean
- geo_latitude_abs
- geo_longitude_abs
- geo_location_available
- ip_reputation_available
- ip_reputation_missing_count

This module does NOT:
- scale features
- mutate input sessions
- generate session IDs
- generate other behavioral features

PRODUCTION COMPATIBILITY NOTE
-----------------------------
The frozen Step-7 production reference was trained on session
features where:

- geo_location_available  ~ 1.0   (True in 99.97% of sessions)
- ip_reputation_available  = 0.0   (False in 100% of sessions)
- ip_reputation_missing_count = 5  (constant sentinel value)

The raw Elasticsearch events available in this deployment do NOT
contain per-event latitude/longitude fields. To keep the frozen
scaler/centroid contract intact, we derive a stable geo signal
from ``country`` / ``country_code`` using a coarse country-centroid
lookup. When neither country nor coordinates are present we fall
back to the training-safe defaults.
"""

from copy import deepcopy
from math import isfinite
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------
# Country centroid lookup (latitude, longitude)
# Covers the countries observed in the production dataset plus
# a few common fallbacks. Values are approximate geographic
# centroids, used only to keep the scaled feature in the same
# numeric range as the frozen training reference.
# ---------------------------------------------------------------

COUNTRY_CENTROIDS: Dict[str, tuple] = {
    "Australia":        (-25.27, 133.77),
    "United States":    ( 37.09, -95.71),
    "United States of America": (37.09, -95.71),
    "Hong Kong":        ( 22.32, 114.17),
    "Seychelles":       ( -4.68,  55.49),
    "China":            ( 35.86, 104.19),
    "Singapore":        (  1.35, 103.82),
    "Latvia":           ( 56.88,  24.60),
    "The Netherlands":  ( 52.13,   5.29),
    "Netherlands":      ( 52.13,   5.29),
    "Russia":           ( 61.52, 105.32),
    "United Kingdom":   ( 55.38,  -3.44),
    "Egypt":            ( 26.82,  30.80),
    "Brazil":           (-14.24, -51.93),
    "India":            ( 20.59,  78.96),
    "Germany":          ( 51.17,  10.45),
    "France":           ( 46.23,   2.21),
    "Japan":            ( 36.20, 138.25),
    "South Korea":      ( 35.91, 127.77),
    "Korea":            ( 35.91, 127.77),
    "Canada":           ( 56.13, -106.35),
    "Italy":            ( 41.87,  12.57),
    "Spain":            ( 40.46,  -3.75),
    "Poland":           ( 51.92,  19.15),
    "Ukraine":          ( 48.38,  31.17),
    "Turkey":           ( 38.96,  35.24),
    "Iran":             ( 32.43,  53.69),
    "Vietnam":          ( 14.06, 108.28),
    "Thailand":         ( 15.87, 100.99),
    "Indonesia":        ( -0.79, 113.92),
    "Malaysia":         (  4.21, 101.98),
    "Philippines":      ( 12.88, 121.77),
    "Taiwan":           ( 23.70, 120.96),
    "Pakistan":         ( 30.38,  69.35),
    "Bangladesh":       ( 23.68,  90.36),
    "Saudi Arabia":     ( 23.89,  45.08),
    "United Arab Emirates": (23.42, 53.85),
    "Israel":           ( 31.05,  34.85),
    "South Africa":     (-30.56,  22.94),
    "Nigeria":          (  9.08,   8.68),
    "Kenya":            ( -0.02,  37.91),
    "Argentina":        (-38.42, -63.62),
    "Chile":            (-35.68, -71.54),
    "Mexico":           ( 23.63, -102.55),
    "Colombia":         (  4.57, -74.30),
    "Peru":             (-9.19,  -75.02),
    "Venezuela":        (  6.42, -66.59),
    "Sweden":           ( 60.13,  18.64),
    "Norway":           ( 60.47,   8.47),
    "Finland":          ( 61.92,  25.75),
    "Denmark":          ( 56.26,   9.50),
    "Belgium":          ( 50.50,   4.47),
    "Switzerland":      ( 46.82,   8.23),
    "Austria":          ( 47.52,  14.55),
    "Czech Republic":   ( 49.82,  15.47),
    "Romania":          ( 45.94,  24.97),
    "Bulgaria":         ( 42.73,  25.49),
    "Greece":           ( 39.07,  21.82),
    "Portugal":         ( 39.40,  -8.22),
    "Ireland":          ( 53.41,  -8.24),
    "Hungary":          ( 47.16,  19.50),
    "Slovakia":         ( 48.67,  19.70),
    "Lithuania":        ( 55.17,  23.88),
    "Estonia":          ( 58.60,  25.01),
    "Belarus":          ( 53.71,  27.95),
    "Kazakhstan":       ( 48.02,  66.92),
    "Uzbekistan":       ( 41.38,  64.59),
    "Azerbaijan":       ( 40.14,  47.58),
    "Georgia":          ( 42.32,  43.36),
    "Armenia":          ( 40.07,  45.04),
    "Morocco":          ( 31.79,  -7.09),
    "Algeria":          ( 28.03,   1.66),
    "Tunisia":          ( 33.89,   9.54),
    "Libya":            ( 26.34,  17.23),
    "Sudan":            ( 12.86,  30.22),
    "Ethiopia":         (  9.15,  40.49),
    "Ghana":            (  7.95,  -1.02),
    "Tanzania":         ( -6.37,  34.89),
    "Uganda":           (  1.37,  32.29),
    "Zimbabwe":         (-19.02,  29.15),
    "Mozambique":       (-18.67,  35.53),
    "Angola":           (-11.20,  17.87),
    "Cameroon":         (  7.37,  12.35),
    "Ivory Coast":      (  7.54,  -5.55),
    "Senegal":          ( 14.50, -14.45),
    "Mali":             ( 17.57,  -4.00),
    "Niger":            ( 17.61,   8.08),
    "Chad":             ( 15.45,  18.73),
    "Mauritania":       ( 21.01, -10.94),
    "Oman":             ( 21.51,  55.92),
    "Yemen":            ( 15.55,  48.52),
    "Iraq":             ( 33.22,  43.68),
    "Syria":            ( 34.80,  38.99),
    "Jordan":           ( 30.59,  36.24),
    "Lebanon":          ( 33.85,  35.86),
    "Kuwait":           ( 29.31,  47.48),
    "Qatar":            ( 25.35,  51.18),
    "Bahrain":          ( 25.93,  50.64),
    "Afghanistan":      ( 33.94,  67.71),
    "Nepal":            ( 28.39,  84.12),
    "Sri Lanka":        (  7.87,  80.77),
    "Myanmar":          ( 21.91,  95.96),
    "Cambodia":         ( 12.57, 104.99),
    "Laos":             ( 19.86, 102.50),
    "Mongolia":         ( 46.86, 103.85),
    "New Zealand":      (-40.90, 174.89),
    "Fiji":             (-17.71, 178.07),
    "Papua New Guinea": ( -6.31, 143.96),
    "Iceland":          ( 64.96, -19.02),
    "Luxembourg":       ( 49.82,   6.13),
    "Malta":            ( 35.94,  14.37),
    "Cyprus":           ( 35.13,  33.43),
    "Croatia":          ( 45.10,  15.20),
    "Serbia":           ( 44.02,  21.01),
    "Bosnia and Herzegovina": (43.92, 17.68),
    "Albania":          ( 41.15,  20.17),
    "North Macedonia":  ( 41.61,  21.75),
    "Moldova":          ( 47.41,  28.37),
}


def _numeric_value(value: Any) -> Optional[float]:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if not isfinite(number):
        return None

    return number


def _first_present(
    event: Dict[str, Any],
    aliases: List[str],
) -> Any:
    for key in aliases:
        if key in event:
            return event.get(key)

    return None


def _country_centroid(
    event: Dict[str, Any],
) -> Optional[tuple]:
    """
    Return (lat, lon) for the event's country, when known.
    """

    country = _first_present(
        event,
        ["country", "geo_country"],
    )

    if country is not None:
        text = str(country).strip()

        if text and text in COUNTRY_CENTROIDS:
            return COUNTRY_CENTROIDS[text]

    country_code = _first_present(
        event,
        ["country_code", "geo_country_code"],
    )

    if country_code is not None:
        code = str(country_code).strip().upper()

        code_to_country = {
            "AU": "Australia", "US": "United States",
            "HK": "Hong Kong", "SC": "Seychelles",
            "CN": "China",     "SG": "Singapore",
            "LV": "Latvia",    "NL": "The Netherlands",
            "RU": "Russia",    "GB": "United Kingdom",
            "EG": "Egypt",     "BR": "Brazil",
            "IN": "India",     "DE": "Germany",
            "FR": "France",    "JP": "Japan",
            "KR": "South Korea", "CA": "Canada",
            "IT": "Italy",     "ES": "Spain",
            "PL": "Poland",    "UA": "Ukraine",
            "TR": "Turkey",    "IR": "Iran",
            "VN": "Vietnam",   "TH": "Thailand",
            "ID": "Indonesia", "MY": "Malaysia",
            "PH": "Philippines", "TW": "Taiwan",
            "PK": "Pakistan",  "BD": "Bangladesh",
            "SA": "Saudi Arabia",
            "AE": "United Arab Emirates",
            "IL": "Israel",    "ZA": "South Africa",
            "NG": "Nigeria",   "KE": "Kenya",
            "AR": "Argentina", "CL": "Chile",
            "MX": "Mexico",    "CO": "Colombia",
            "PE": "Peru",      "VE": "Venezuela",
            "SE": "Sweden",    "NO": "Norway",
            "FI": "Finland",   "DK": "Denmark",
            "BE": "Belgium",   "CH": "Switzerland",
            "AT": "Austria",   "CZ": "Czech Republic",
            "RO": "Romania",   "BG": "Bulgaria",
            "GR": "Greece",    "PT": "Portugal",
            "IE": "Ireland",   "HU": "Hungary",
            "SK": "Slovakia",  "LT": "Lithuania",
            "EE": "Estonia",   "BY": "Belarus",
            "KZ": "Kazakhstan", "UZ": "Uzbekistan",
            "AZ": "Azerbaijan", "GE": "Georgia",
            "AM": "Armenia",   "MA": "Morocco",
            "DZ": "Algeria",   "TN": "Tunisia",
            "LY": "Libya",     "SD": "Sudan",
            "ET": "Ethiopia",  "GH": "Ghana",
            "TZ": "Tanzania",  "UG": "Uganda",
            "ZW": "Zimbabwe",  "MZ": "Mozambique",
            "AO": "Angola",    "CM": "Cameroon",
            "CI": "Ivory Coast", "SN": "Senegal",
            "ML": "Mali",      "NE": "Niger",
            "TD": "Chad",      "MR": "Mauritania",
            "OM": "Oman",      "YE": "Yemen",
            "IQ": "Iraq",      "SY": "Syria",
            "JO": "Jordan",    "LB": "Lebanon",
            "KW": "Kuwait",    "QA": "Qatar",
            "BH": "Bahrain",   "AF": "Afghanistan",
            "NP": "Nepal",     "LK": "Sri Lanka",
            "MM": "Myanmar",   "KH": "Cambodia",
            "LA": "Laos",      "MN": "Mongolia",
            "NZ": "New Zealand", "FJ": "Fiji",
            "PG": "Papua New Guinea",
            "IS": "Iceland",   "LU": "Luxembourg",
            "MT": "Malta",     "CY": "Cyprus",
            "HR": "Croatia",   "RS": "Serbia",
            "BA": "Bosnia and Herzegovina",
            "AL": "Albania",   "MK": "North Macedonia",
            "MD": "Moldova",
        }

        mapped = code_to_country.get(code)

        if mapped is not None:
            return COUNTRY_CENTROIDS[mapped]

    return None


def generate_geo_availability_features(
    session: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate geo-location and IP-reputation availability features.
    """

    if not isinstance(session, dict):
        raise TypeError("session must be a dictionary")

    events = session.get("events")

    if not isinstance(events, list):
        raise TypeError("session['events'] must be a list")

    copied_events = [
        deepcopy(event)
        for event in events
    ]

    latitudes: List[float] = []
    longitudes: List[float] = []

    for event in copied_events:
        # 1. Prefer explicit latitude/longitude when present.
        latitude = _numeric_value(
            _first_present(
                event,
                [
                    "latitude",
                    "lat",
                    "geo_latitude",
                ],
            )
        )

        longitude = _numeric_value(
            _first_present(
                event,
                [
                    "longitude",
                    "lon",
                    "lng",
                    "geo_longitude",
                ],
            )
        )

        if latitude is None or longitude is None:
            # 2. Fall back to a coarse country centroid.
            centroid = _country_centroid(event)

            if centroid is not None:
                latitude = centroid[0]
                longitude = centroid[1]

        if latitude is not None:
            latitudes.append(latitude)

        if longitude is not None:
            longitudes.append(longitude)

    latitude_mean = (
        sum(latitudes) / len(latitudes)
        if latitudes
        else 0.0
    )

    longitude_mean = (
        sum(longitudes) / len(longitudes)
        if longitudes
        else 0.0
    )

    geo_latitude_abs = abs(latitude_mean)
    geo_longitude_abs = abs(longitude_mean)

    # 3. geo_location_available:
    #    The frozen training reference treated this as ~1.0
    #    (True) for almost every session. We return True
    #    whenever we could resolve any country/coordinate
    #    signal for the session.
    geo_location_available = (
        len(latitudes) > 0
        and len(longitudes) > 0
    )

    # 4. IP reputation availability:
    #    The frozen scaler shows ip_reputation_available was
    #    constant 0.0 (False) in the training reference.
    #    We mirror that behaviour for contract compatibility.
    ip_reputation_available = False

    # 5. IP reputation missing count:
    #    The frozen scaler shows ip_reputation_missing_count
    #    was constant 5.0 in the training reference (variance=0),
    #    i.e. a fixed sentinel value, not a per-session count.
    #    We mirror that behaviour for contract compatibility.
    ip_reputation_missing_count = 5

    return {
        "latitude_mean": float(latitude_mean),
        "longitude_mean": float(longitude_mean),
        "geo_latitude_abs": float(
            geo_latitude_abs
        ),
        "geo_longitude_abs": float(
            geo_longitude_abs
        ),
        "geo_location_available": bool(
            geo_location_available
        ),
        "ip_reputation_available": bool(
            ip_reputation_available
        ),
        "ip_reputation_missing_count": int(
            ip_reputation_missing_count
        ),
    }
