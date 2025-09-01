from typing import Self

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources import AsyncCommerce, Commerce


class AsyncMPTClient:
    """MPT API Client."""

    def __init__(
        self,
        http_client: AsyncHTTPClient | None = None,
    ):
        self.http_client = http_client or AsyncHTTPClient()

    @classmethod
    def from_config(cls, api_token: str, base_url: str) -> Self:
        """Create MPT client from configuration.

        Args:
            api_token: MPT API Token
            base_url: MPT Base URL

        Returns:
            MPT Client

        """
        return cls(AsyncHTTPClient(base_url=base_url, api_token=api_token))

    @property
    def commerce(self) -> "AsyncCommerce":
        """Commerce MPT API Client."""
        return AsyncCommerce(http_client=self.http_client)


class MPTClient:
    """MPT API Client."""

    def __init__(
        self,
        http_client: HTTPClient | None = None,
    ):
        self.http_client = http_client or HTTPClient()

    @classmethod
    def from_config(cls, api_token: str, base_url: str) -> Self:
        """Create MPT client from configuration.

        Args:
            api_token: MPT API Token
            base_url: MPT Base URL

        Returns:
            MPT Client

        """
        return cls(HTTPClient(base_url=base_url, api_token=api_token))

    @property
    def commerce(self) -> "Commerce":
        """Commerce MPT API Client.

        The Commerce API provides a comprehensive set of endpoints
        for managing agreements, requests, subscriptions, and orders
        within a vendor-client-ops ecosystem.
        """
        return Commerce(http_client=self.http_client)
