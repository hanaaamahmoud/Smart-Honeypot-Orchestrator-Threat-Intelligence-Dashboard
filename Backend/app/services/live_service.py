from app.services.es_client import es_client, ES_INDEX

def get_live_kpis():
    total_events = es_client.count(index=ES_INDEX)["count"]

    unique_ips = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "unique_ips": {"cardinality": {"field": "source_ip"}},
                "unique_countries": {"cardinality": {"field": "country"}},
                "unique_honeypots": {"cardinality": {"field": "honeypot"}}
            }
        }
    )

    return {
        "totalEvents": total_events,
        "uniqueIPs": unique_ips["aggregations"]["unique_ips"]["value"],
        "uniqueCountries": unique_ips["aggregations"]["unique_countries"]["value"],
        "activeHoneypots": unique_ips["aggregations"]["unique_honeypots"]["value"]
    }



def get_by_honeypot():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "by_honeypot": {
                    "terms": {"field": "honeypot", "size": 10}
                }
            }
        }
    )

    buckets = result["aggregations"]["by_honeypot"]["buckets"]

    return [
        {"name": b["key"], "value": b["doc_count"]}
        for b in buckets
    ]



def get_by_protocol():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "by_protocol": {
                    "terms": {"field": "protocol", "size": 10}
                }
            }
        }
    )

    buckets = result["aggregations"]["by_protocol"]["buckets"]

    return [
        {"name": b["key"], "value": b["doc_count"]}
        for b in buckets
    ]


def get_by_severity():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "by_severity": {
                    "terms": {"field": "severity", "size": 10}
                }
            }
        }
    )

    buckets = result["aggregations"]["by_severity"]["buckets"]

    return [
        {"name": b["key"], "value": b["doc_count"]}
        for b in buckets
    ]


def get_by_country():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "by_country": {
                    "terms": {"field": "country", "size": 20}
                }
            }
        }
    )

    buckets = result["aggregations"]["by_country"]["buckets"]

    return [
        {"name": b["key"], "value": b["doc_count"]}
        for b in buckets
    ]



def get_top_attackers():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "top_attackers": {
                    "terms": {"field": "source_ip", "size": 20}
                }
            }
        }
    )

    buckets = result["aggregations"]["top_attackers"]["buckets"]

    return [
        {"ip": b["key"], "count": b["doc_count"]}
        for b in buckets
    ]


def get_by_mitre():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "by_mitre": {
                    "terms": {"field": "mitre_technique", "size": 15}
                }
            }
        }
    )

    buckets = result["aggregations"]["by_mitre"]["buckets"]

    return [
        {"name": b["key"], "value": b["doc_count"]}
        for b in buckets
    ]


def get_timeline():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "events_over_time": {
                    "date_histogram": {
                        "field": "timestamp",
                        "calendar_interval": "day"
                    }
                }
            }
        }
    )

    buckets = result["aggregations"]["events_over_time"]["buckets"]

    return [
        {"date": b["key_as_string"], "count": b["doc_count"]}
        for b in buckets
    ]


def get_recent_events():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 50,
            "sort": [
                {"timestamp": {"order": "desc"}}
            ]
        }
    )

    hits = result["hits"]["hits"]

    return [hit["_source"] for hit in hits]


def get_by_reputation():
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "by_reputation": {
                    "terms": {"field": "ip_reputation_level", "size": 10}
                }
            }
        }
    )

    buckets = result["aggregations"]["by_reputation"]["buckets"]

    return [
        {"name": b["key"], "value": b["doc_count"]}
        for b in buckets
    ]