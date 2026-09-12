import json
import urllib.request


def test_health():
    request = urllib.request.Request(
        "http://localhost:8000/health",
        method="GET",
    )

    with urllib.request.urlopen(request) as response:
        assert response.status == 200
        data = json.loads(response.read().decode("utf-8"))

    assert data["status"] == "ok"
