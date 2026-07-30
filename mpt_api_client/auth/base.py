"""Generic authentication providers for the MPT API client.

Providers are :class:`httpx.Auth` subclasses, so the same implementation is used by both
the sync and the async HTTP clients.
"""

import os
from collections.abc import Generator
from typing import override

import httpx

from mpt_api_client.exceptions import MPTError
from mpt_api_client.http.transport_settings import TransportSettings


class Authentication(httpx.Auth):
    """Base class for MPT API authentication providers."""

    def configure(self, transport: TransportSettings) -> None:
        """Receive the owning HTTP client's transport settings.

        Called once by ``HTTPClient``/``AsyncHTTPClient`` at construction time. The base
        implementation is a no-op; providers that need the client's configuration
        override it.

        Args:
            transport: Resolved transport settings of the owning client.
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


class EnvTokenAuthentication(BearerTokenAuthentication):
    """Bearer token authentication that reads the token from the environment.

    The token is resolved from the ``MPT_API_TOKEN`` environment variable (or the
    variable named by ``env_var``) at construction time.
    """

    def __init__(self, env_var: str = "MPT_API_TOKEN") -> None:
        """Initialize the provider from the environment.

        Args:
            env_var: Name of the environment variable holding the API token.

        Raises:
            MPTError: If the environment variable is not set or empty.
        """
        token = os.getenv(env_var)
        if not token:
            raise MPTError(f"Environment variable '{env_var}' is not set.")
        super().__init__(token)
