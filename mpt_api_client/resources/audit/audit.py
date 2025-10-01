from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.audit.event_types import (
    AsyncEventTypesService,
    EventTypesService,
)
from mpt_api_client.resources.audit.records import AsyncRecordsService, RecordsService


class Audit:
    """Audit MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def records(self) -> RecordsService:
        """Records service."""
        return RecordsService(http_client=self.http_client)

    @property
    def event_types(self) -> EventTypesService:
        """Event Types service."""
        return EventTypesService(http_client=self.http_client)


class AsyncAudit:
    """Async Audit MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def records(self) -> AsyncRecordsService:
        """Records service."""
        return AsyncRecordsService(http_client=self.http_client)

    @property
    def event_types(self) -> AsyncEventTypesService:
        """Event Types service."""
        return AsyncEventTypesService(http_client=self.http_client)
