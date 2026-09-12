"""
Elasticsearch input adapter.

Production source:
    Elasticsearch / honeypot-events

This module will only READ events.

It must never modify the ML model.
"""


class ElasticsearchReader:

    def __init__(
        self,
        url: str,
        index: str,
    ):
        self.url = url
        self.index = index

    def health(self):
        raise NotImplementedError(
            "Elasticsearch connection will be implemented "
            "during real ELK integration."
        )

    def read_events(self, *args, **kwargs):
        raise NotImplementedError(
            "Elasticsearch event reader will be implemented "
            "during real ELK integration."
        )
