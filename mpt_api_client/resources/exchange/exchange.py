from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.exchange.currencies import (
    AsyncCurrenciesService,
    CurrenciesService,
)


class Exchange:
    """Exchange MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def currencies(self) -> CurrenciesService:
        """Currencies service."""
        return CurrenciesService(http_client=self.http_client)


class AsyncExchange:
    """Exchange MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def currencies(self) -> AsyncCurrenciesService:
        """Currencies service."""
        return AsyncCurrenciesService(http_client=self.http_client)
