from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.integration.categories import (
    AsyncCategoriesService,
    CategoriesService,
)
from mpt_api_client.resources.integration.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


class Integration:
    """Integration MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def extensions(self) -> ExtensionsService:
        """Extensions service."""
        return ExtensionsService(http_client=self.http_client)

    @property
    def categories(self) -> CategoriesService:
        """Categories service."""
        return CategoriesService(http_client=self.http_client)


class AsyncIntegration:
    """Async Integration MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def extensions(self) -> AsyncExtensionsService:
        """Extensions service."""
        return AsyncExtensionsService(http_client=self.http_client)

    @property
    def categories(self) -> AsyncCategoriesService:
        """Categories service."""
        return AsyncCategoriesService(http_client=self.http_client)
