from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.commerce.orders import AsyncOrdersService, OrdersService


class Commerce:
    """Commerce MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def orders(self) -> OrdersService:
        """Order service."""
        return OrdersService(http_client=self.http_client)


class AsyncCommerce:
    """Commerce MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def orders(self) -> AsyncOrdersService:
        """Order service."""
        return AsyncOrdersService(http_client=self.http_client)
