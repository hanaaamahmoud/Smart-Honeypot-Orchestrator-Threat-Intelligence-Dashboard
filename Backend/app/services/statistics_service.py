from app.services.es_client import es_client, ES_INDEX

def get_total_attacks():
    result = es_client.count(index=ES_INDEX)
    return result["count"]

def get_statistics():
    total = get_total_attacks()


    unique_attackers = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "unique_ips": {"cardinality": {"field": "source_ip.keyword"}}
            }
        }
    )
    unique_ips = unique_attackers["aggregations"]["unique_ips"]["value"]


    top_countries = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "countries": {
                    "terms": {"field": "country.keyword", "size": 10}
                }
            }
        }
    )
    countries = [
        {"country": b["key"], "count": b["doc_count"]}
        for b in top_countries["aggregations"]["countries"]["buckets"]
    ]

    return {
        "totalAttacks": total,
        "uniqueAttackers": unique_ips,
        "topCountries": countries
    }


def get_recent_events(size=10):
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": size,
            "sort": [{"timestamp": {"order": "desc"}}],
            "query": {"match_all": {}}
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]


def get_top_attackers(size=10):
    result = es_client.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "aggs": {
                "top_attackers": {
                    "terms": {"field": "source_ip.keyword", "size": size}
                }
            }
        }
    )
    return [
        {"ip": b["key"], "count": b["doc_count"]}
        for b in result["aggregations"]["top_attackers"]["buckets"]
    ]