import asyncio
from app.services.es_client import es_client, ES_INDEX

last_timestamp = None

async def produce_events(manager):
    global last_timestamp
    while True:
        query = {"match_all": {}}
        if last_timestamp:
            query = {"range": {"timestamp": {"gt": last_timestamp}}}

        result = es_client.search(
            index=ES_INDEX,
            body={
                "size": 50,
                "sort": [{"timestamp": {"order": "asc"}}],
                "query": query
            }
        )

        for hit in result["hits"]["hits"]:
            event = hit["_source"]
            await manager.broadcast(event)
            last_timestamp = event["timestamp"]

        await asyncio.sleep(5)