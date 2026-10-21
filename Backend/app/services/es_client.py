from elasticsearch import Elasticsearch
import os

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "honeypot-events")

es_client = Elasticsearch(ES_HOST, request_timeout=30)

def check_es_connection():
    if not es_client.ping():
        raise ConnectionError("Cannot connect to Elasticsearch")