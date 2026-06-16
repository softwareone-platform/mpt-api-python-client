"""Generic authentication providers for the MPT API client.

Providers are :class:`httpx.Auth` subclasses, so the same implementation is used by both
the sync and the async HTTP clients.
"""

from collections.abc import Generator
from typing import override

import httpx


class Authentication(httpx.Auth):
    """Base class for MPT API authentication providers."""

    def configure(self, *, base_url: str, timeout: float, retries: int) -> None:
        """Receive the owning HTTP client's configuration.

        Called once by ``HTTPClient``/``AsyncHTTPClient`` at construction time. The base
        implementation is a no-op; providers that need the client's configuration (such as
        ``ExtensionFrameworkAuthentication``) override it.

        Args:
            base_url: Resolved base URL of the owning client.
            timeout: HTTP request timeout in seconds.
            retries: Number of retries configured on the owning client.
        """


class BearerTokenAuthentication(Authentication):
    """Authenticate every request with a single long-lived bearer token."""

    def __init__(self, token: str) -> None:
        self._token = token

    @override
    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Attach the bearer token to the outgoing request."""
        request.headers["Authorization"] = f"Bearer {self._token}"
        yield request
