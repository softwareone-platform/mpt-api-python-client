"""Generic authentication providers for the MPT API client.

Providers are :class:`httpx.Auth` subclasses, so the same implementation is used by both
the sync and the async HTTP clients.
"""

from collections.abc import Generator
from typing import override

import httpx

from mpt_api_client.config import ClientConfig


class Authentication(httpx.Auth):
    """Base class for MPT API authentication providers."""

    def configure(self, config: ClientConfig) -> ClientConfig:
        """Receive the owning HTTP client's configuration and optionally amend it.

        Called once by ``HTTPClient``/``AsyncHTTPClient`` at construction time, before
        the base URL falls back to ``MPT_API_BASE_URL`` and is validated. Providers
        bound to a specific environment may fill ``base_url`` when it is ``None``;
        explicitly passed values should be preserved. The base implementation returns
        the configuration unchanged.

        Args:
            config: Configuration of the owning client as passed by the caller.

        Returns:
            The configuration to use, possibly amended.
        """
        return config


class BearerTokenAuthentication(Authentication):
    """Authenticate every request with a single long-lived bearer token."""

    def __init__(self, token: str) -> None:
        self._token = token

    @override
    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Attach the bearer token to the outgoing request."""
        request.headers["Authorization"] = f"Bearer {self._token}"
        yield request
