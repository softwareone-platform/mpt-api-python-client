"""Authentication providers for the MPT API client.

Providers are :class:`httpx.Auth` subclasses, so the same implementation is used by both
the sync and the async HTTP clients. Token-refresh requests are yielded back through the
owning client, reusing its ``base_url``, retry policy and transport.
"""

from collections.abc import Generator
from typing import override

import httpx

DEFAULT_TOKEN_URL = "/public/v1/integration/installations/-/token"  # noqa: S105


class Authentication(httpx.Auth):
    """Base class for MPT API authentication providers."""


class BearerTokenAuthentication(Authentication):
    """Authenticate every request with a single long-lived bearer token."""

    def __init__(self, token: str) -> None:
        self._token = token

    @override
    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Attach the bearer token to the outgoing request."""
        request.headers["Authorization"] = f"Bearer {self._token}"
        yield request


class ExtensionFrameworkAuthentication(Authentication):
    """Authenticate with a short-lived installation token.

    The token is fetched from the token endpoint using the extension secret, cached, and
    refreshed reactively whenever a request comes back with ``401 Unauthorized``.

    Note:
        This provider is not thread-safe; the cached token is shared without locking.
    """

    requires_response_body = True  # read the token / 401 body inside the auth flow

    def __init__(self, secret: str, token_url: str = DEFAULT_TOKEN_URL) -> None:
        self._secret = secret
        self._token_url = token_url
        self._token: str | None = None

    @override
    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Attach a cached installation token, refreshing it on demand and on 401."""
        if self._token is None:
            yield from self._fetch_token(request)
        request.headers["Authorization"] = f"Bearer {self._token}"
        response = yield request
        if response.status_code == httpx.codes.UNAUTHORIZED:
            yield from self._fetch_token(request)
            request.headers["Authorization"] = f"Bearer {self._token}"
            yield request

    def _fetch_token(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Request a fresh installation token and cache it."""
        token_request = httpx.Request(
            "POST",
            request.url.join(self._token_url),
            headers={"Authorization": f"Bearer {self._secret}"},
        )
        token_response = yield token_request
        token_response.raise_for_status()
        self._token = token_response.json()["token"]
