from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.extensibility.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


class Extensibility:
    """Extensibility MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def extensions(self) -> ExtensionsService:
        """Extensions service."""
        return ExtensionsService(http_client=self.http_client)


class AsyncExtensibility:
    """Async Extensibility MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def extensions(self) -> AsyncExtensionsService:
        """Extensions service."""
        return AsyncExtensionsService(http_client=self.http_client)
