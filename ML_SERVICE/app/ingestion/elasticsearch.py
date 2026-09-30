"""
Elasticsearch input reader.

Production source:
    Elasticsearch / honeypot-events

Responsibilities:
    - Connect to Elasticsearch.
    - Verify Elasticsearch availability.
    - Read raw events from the configured index.
    - Read events in controlled batches.
    - Keep the reader read-only.
    - Return Elasticsearch _source documents only.

Non-responsibilities:
    - No normalization.
    - No session reconstruction.
    - No feature generation.
    - No ML inference.
    - No clustering.
    - No training/retraining.
    - No writes to Elasticsearch.
"""

from typing import Any, Dict, Iterator, List, Optional

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


class ElasticsearchReader:
    """Read-only Elasticsearch reader for real honeypot events."""

    def __init__(self, url: str, index: str, timeout: int = 10):
        self.url = url
        self.index = index
        self.timeout = timeout

        self.client = Elasticsearch(
            self.url,
            request_timeout=self.timeout,
        )

    def health(self) -> Dict[str, Any]:
        """Check Elasticsearch availability and return basic cluster information."""
        try:
            info = self.client.info()

            return {
                "status": "ok",
                "name": info.get("name"),
                "cluster_name": info.get("cluster_name"),
                "version": info.get("version", {}).get("number"),
            }

        except Exception as exc:
            raise RuntimeError(
                f"Elasticsearch is unavailable at {self.url}: {exc}"
            ) from exc

    def count(self) -> int:
        """Return the number of documents in the configured index."""
        try:
            response = self.client.count(index=self.index)

            return int(response["count"])

        except Exception as exc:
            raise RuntimeError(
                f"Unable to count documents in index "
                f"'{self.index}': {exc}"
            ) from exc

    def read_events(
        self,
        size: int = 100,
        query: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Read a limited number of events from Elasticsearch.

        This method performs a normal search and returns only the
        Elasticsearch _source documents.
        """
        if size <= 0:
            return []

        if query is None:
            query = {"match_all": {}}

        try:
            response = self.client.search(
                index=self.index,
                query=query,
                size=size,
            )

            hits = response.get("hits", {}).get("hits", [])

            events = []

            for hit in hits:
                source = hit.get("_source")

                if source is not None:
                    events.append(source)

            return events

        except Exception as exc:
            raise RuntimeError(
                f"Unable to read events from index "
                f"'{self.index}': {exc}"
            ) from exc

    def read_events_in_batches(
        self,
        batch_size: int = 100,
        query: Optional[Dict[str, Any]] = None,
    ) -> Iterator[List[Dict[str, Any]]]:
        """
        Read all matching events from Elasticsearch in controlled batches.

        The method is read-only and returns only Elasticsearch _source
        documents. It does not perform normalization, ML processing,
        clustering, training, or writes.

        Args:
            batch_size:
                Maximum number of events returned per batch.

            query:
                Elasticsearch query body without the outer "query" key.
                Defaults to match_all.

        Yields:
            Lists of raw Elasticsearch _source documents.
        """
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0")

        if query is None:
            query = {"match_all": {}}

        try:
            batch: List[Dict[str, Any]] = []

            for hit in scan(
                self.client,
                index=self.index,
                query={"query": query},
                size=batch_size,
                preserve_order=False,
            ):
                source = hit.get("_source")

                if source is None:
                    continue

                batch.append(source)

                if len(batch) >= batch_size:
                    yield batch
                    batch = []

            if batch:
                yield batch

        except Exception as exc:
            raise RuntimeError(
                f"Unable to read events in batches from index "
                f"'{self.index}': {exc}"
            ) from exc
