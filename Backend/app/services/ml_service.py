import json
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ml_analytics"

@lru_cache(maxsize=None)
def load_analytics(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def load_replay_detail(session_id: str) -> dict:
    path = DATA_DIR / "session_replay_details" / f"{session_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"No replay: {session_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def get_clusters():
    return load_analytics("cluster_analytics.json")


def get_temporal():
    return load_analytics("temporal_analytics.json")


def get_session_summary():
    return load_analytics("session_analytics.json")


def get_alerts():
    data = load_analytics("session_analytics.json")
    return {
        "count": data.get("critical_alerts_count", 0),
        "alerts": data.get("critical_alerts", []),
    }


def get_top_attackers():
    data = load_analytics("session_analytics.json")
    return {"attackers": data.get("top_source_ips", [])}


def get_mitre():
    return load_analytics("mitre_analytics.json")


def get_mitre_statistics():
    return load_analytics("mitre_statistics.json")


def get_mitre_trends():
    return load_analytics("mitre_trends.json")


def get_replay_list():
    return load_analytics("session_replay_list.json")