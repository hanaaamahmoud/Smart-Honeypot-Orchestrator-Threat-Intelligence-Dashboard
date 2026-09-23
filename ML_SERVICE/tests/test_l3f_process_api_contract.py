import json
import urllib.error
import urllib.request


BASE_URL = "http://localhost:8000/process"


def post_json(payload):
    request = urllib.request.Request(
        BASE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(
                response.read().decode("utf-8")
            )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = body

        return exc.code, payload


def valid_event(session_id="l3f-session-001"):
    return {
        "timestamp": "2025-01-01T00:00:00Z",
        "event_type": "auth",
        "source_ip": "10.0.0.10",
        "username": "admin",
        "session_id": session_id,
        "protocol": "SSH",
        "honeypot": "cowrie",
    }


def test_l3f_valid_request():
    status, result = post_json(
        {"events": [valid_event()]}
    )

    assert status == 200
    assert result["status"] == "ok"
    assert result["sessions_processed"] == 1
    assert len(result["results"]) == 1


def test_l3f_empty_events():
    status, result = post_json(
        {"events": []}
    )

    assert status == 200
    assert result["status"] == "ok"
    assert result["sessions_processed"] == 0
    assert result["results"] == []


def test_l3f_malformed_request_missing_events():
    status, result = post_json({})

    assert status == 422
    assert isinstance(result, dict)
    assert "detail" in result


def test_l3f_malformed_request_events_not_list():
    status, result = post_json(
        {"events": "not-a-list"}
    )

    assert status == 422
    assert isinstance(result, dict)
    assert "detail" in result


def test_l3f_partial_event_does_not_fabricate_optional_values():
    event = valid_event()
    event.pop("protocol")
    event.pop("honeypot")

    status, result = post_json(
        {"events": [event]}
    )

    assert status == 200
    assert result["status"] == "ok"
    assert result["sessions_processed"] == 1

    item = result["results"][0]

    assert item["protocol"] is None
    assert item["honeypot"] is None
    assert item["source"] is None
