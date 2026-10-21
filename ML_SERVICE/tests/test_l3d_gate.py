import json
import urllib.request


def test_production_output_is_ready():
    request = urllib.request.Request(
        "http://localhost:8000/ready",
        method="GET",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    assert result["status"] == "ready"
    assert result["ready"] is True
    assert result["model_loaded"] is True
    assert result["scaler_loaded"] is True
    assert result["feature_contract_loaded"] is True
    assert result["reference_clusters_loaded"] is True
