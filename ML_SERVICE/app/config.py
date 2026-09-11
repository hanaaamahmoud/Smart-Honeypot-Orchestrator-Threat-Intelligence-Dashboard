"""
Production ML Service Configuration.

IMPORTANT:
- Frozen production ML artifacts are read-only.
- No model retraining is allowed.
- No DBSCAN fitting is allowed.
- No new cluster creation is allowed.
"""

import os


class Settings:
    APP_NAME = os.getenv(
        "ML_SERVICE_NAME",
        "honeypot-ml-service"
    )

    HOST = os.getenv(
        "ML_SERVICE_HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "ML_SERVICE_PORT",
            "8002"
        )
    )

    ELASTICSEARCH_URL = os.getenv(
        "ELASTICSEARCH_URL",
        "http://elasticsearch:9200"
    )

    ELASTICSEARCH_INDEX = os.getenv(
        "ELASTICSEARCH_INDEX",
        "honeypot-events"
    )

    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "http://backend:8001"
    )

    PRODUCTION_MODE = os.getenv(
        "ML_PRODUCTION_MODE",
        "FROZEN_PRODUCTION_REFERENCE"
    )

    FEATURE_COUNT = 48

    ASSIGNMENT_METHOD = (
        "nearest_behavioral_centroid"
    )

    DBSCAN_FITTING_ALLOWED = False
    RETRAINING_ALLOWED = False
    NEW_CLUSTER_CREATION_ALLOWED = False


settings = Settings()
