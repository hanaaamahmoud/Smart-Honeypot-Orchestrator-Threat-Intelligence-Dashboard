import json, sys, requests

ES = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:9201"
INDEX = "honeypot-events"
PER_HONEYPOT = 200     
total = 0
with open("elk/sample/sample-events.ndjson", "w", encoding="utf-8", newline="\n") as f:
    for hp in ["cowrie", "dionaea", "tanner"]:
        body = {
            "size": PER_HONEYPOT,
            "query": {"function_score": {
                "query": {"match": {"honeypot": hp}},
                "random_score": {}
            }}
        }
        r = requests.post(f"{ES}/{INDEX}/_search", json=body, timeout=60)
        r.raise_for_status()
        hits = r.json()["hits"]["hits"]
        for h in hits:
            f.write(json.dumps({"index": {"_index": INDEX}}) + "\n")
            f.write(json.dumps(h["_source"]) + "\n")
        print(f"{hp}: {len(hits)} events")
        total += len(hits)

print("total:", total)