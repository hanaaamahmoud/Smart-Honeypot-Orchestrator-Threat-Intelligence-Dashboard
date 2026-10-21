import pytest

from app.ingestion.elasticsearch import ElasticsearchReader


class FakeClient:
    def __init__(self):
        self.info_calls = 0
        self.count_calls = 0
        self.search_calls = 0

    def info(self):
        self.info_calls += 1

        return {
            "name": "fake-node",
            "cluster_name": "fake-cluster",
            "version": {
                "number": "8.19.2"
            },
        }

    def count(self, index):
        self.count_calls += 1

        return {
            "count": 42
        }

    def search(self, index, query, size):
        self.search_calls += 1

        return {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "source_ip": "192.0.2.10",
                            "protocol": "ftp",
                            "username": "test-user",
                            "password": "test-password",
                        }
                    }
                ]
            }
        }


def make_reader():
    reader = ElasticsearchReader(
        url="http://fake-elasticsearch:9200",
        index="honeypot-events",
    )

    reader.client = FakeClient()

    return reader


def test_health():
    reader = make_reader()

    result = reader.health()

    assert result["status"] == "ok"
    assert result["name"] == "fake-node"
    assert result["cluster_name"] == "fake-cluster"
    assert result["version"] == "8.19.2"


def test_count():
    reader = make_reader()

    result = reader.count()

    assert result == 42


def test_read_events():
    reader = make_reader()

    events = reader.read_events(size=1)

    assert len(events) == 1
    assert isinstance(events[0], dict)


def test_correct_index():
    reader = make_reader()

    assert reader.index == "honeypot-events"


def test_empty_result():
    reader = make_reader()

    reader.client.search = lambda index, query, size: {
        "hits": {
            "hits": []
        }
    }

    events = reader.read_events(size=10)

    assert events == []


def test_raw_fields_preserved():
    reader = make_reader()

    events = reader.read_events(size=1)

    event = events[0]

    assert event["source_ip"] == "192.0.2.10"
    assert event["protocol"] == "ftp"
    assert event["username"] == "test-user"
    assert event["password"] == "test-password"


def test_read_events_does_not_write():
    reader = make_reader()

    before = reader.client.search_calls

    reader.read_events(size=1)

    after = reader.client.search_calls

    assert after == before + 1

    forbidden_methods = [
        "index",
        "create",
        "update",
        "delete",
        "bulk",
        "delete_by_query",
        "update_by_query",
    ]

    public_reader_methods = [
        name
        for name in dir(reader)
        if not name.startswith("_")
        and callable(getattr(reader, name))
    ]

    for method in forbidden_methods:
        assert method not in public_reader_methods


def test_invalid_batch_size():
    reader = make_reader()

    with pytest.raises(ValueError):
        list(
            reader.read_events_in_batches(
                batch_size=0
            )
        )


def test_batching_empty_result():
    reader = make_reader()

    def fake_scan(*args, **kwargs):
        return iter([])

    import app.ingestion.elasticsearch as module

    original_scan = module.scan
    module.scan = fake_scan

    try:
        batches = list(
            reader.read_events_in_batches(
                batch_size=100
            )
        )

        assert batches == []

    finally:
        module.scan = original_scan
