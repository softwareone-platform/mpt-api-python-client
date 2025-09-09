from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService


class Catalog:
    """Catalog MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def products(self) -> ProductsService:
        """Products service."""
        return ProductsService(http_client=self.http_client)


class AsyncCatalog:
    """Catalog MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def products(self) -> AsyncProductsService:
        """Products service."""
        return AsyncProductsService(http_client=self.http_client)
