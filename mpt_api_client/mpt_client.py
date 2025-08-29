from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources import AsyncCommerce, Commerce


class AsyncMPTClient:
    """MPT API Client."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        http_client: AsyncHTTPClient | None = None,
    ):
        self.http_client = http_client or AsyncHTTPClient(base_url=base_url, api_token=api_key)

    @property
    def commerce(self) -> "AsyncCommerce":
        """Commerce MPT API Client."""
        return AsyncCommerce(http_client=self.http_client)


class MPTClient:
    """MPT API Client."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        http_client: HTTPClient | None = None,
    ):
        self.http_client = http_client or HTTPClient(base_url=base_url, api_token=api_key)

    @property
    def commerce(self) -> "Commerce":
        """Commerce MPT API Client.

        The Commerce API provides a comprehensive set of endpoints
        for managing agreements, requests, subscriptions, and orders
        within a vendor-client-ops ecosystem.
        """
        return Commerce(http_client=self.http_client)
