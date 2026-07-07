"""Generic authentication providers for the MPT API client.

Providers are :class:`httpx.Auth` subclasses, so the same implementation is used by both
the sync and the async HTTP clients.
"""

import datetime as dt
from collections.abc import Generator
from typing import override

import httpx

from mpt_api_client.auth.jwt import (
    JWTClaimsError,
    JWTFormatError,
    decode_unverified_jwt_claims,
)
from mpt_api_client.exceptions import MPTError
from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.integration.installations_token import (
    AsyncInstallationsTokenService,
    InstallationsTokenService,
)

DEFAULT_TOKEN_CLIENT_TIMEOUT_SECONDS = 20.0
DEFAULT_TOKEN_CLIENT_RETRIES = 5


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


class InstallationTokenAuthentication(Authentication):
    """Base for providers backed by the integration installations token endpoint.

    Holds the extension secret, captures the owning client's configuration through
    :meth:`configure`, and lazily builds a dedicated token client (authenticated with the
    extension secret) that hosts :class:`InstallationsTokenService` and its async counterpart.
    Subclasses implement the caching and ``auth_flow`` behavior.
    """

    def __init__(self, secret: str) -> None:
        """Initialize the provider.

        Args:
            secret: Extension secret used to authenticate token requests.
        """
        self._secret = secret
        self._base_url: str | None = None
        self._timeout: float = DEFAULT_TOKEN_CLIENT_TIMEOUT_SECONDS
        self._retries: int = DEFAULT_TOKEN_CLIENT_RETRIES
        self._sync_service: InstallationsTokenService | None = None
        self._async_service: AsyncInstallationsTokenService | None = None

    @override
    def configure(self, *, base_url: str, timeout: float, retries: int) -> None:
        """Store the owning client's configuration used to build the token client."""
        self._base_url = base_url
        self._timeout = timeout
        self._retries = retries

    def _get_sync_service(self) -> InstallationsTokenService:
        """Return the cached sync token service, building it on first use."""
        if self._sync_service is None:
            token_client = HTTPClient(
                authentication=BearerTokenAuthentication(self._secret),
                base_url=self._require_base_url(),
                timeout=self._timeout,
                retries=self._retries,
            )
            self._sync_service = InstallationsTokenService(http_client=token_client)
        return self._sync_service

    def _get_async_service(self) -> AsyncInstallationsTokenService:
        """Return the cached async token service, building it on first use."""
        if self._async_service is None:
            token_client = AsyncHTTPClient(
                authentication=BearerTokenAuthentication(self._secret),
                base_url=self._require_base_url(),
                timeout=self._timeout,
                retries=self._retries,
            )
            self._async_service = AsyncInstallationsTokenService(http_client=token_client)
        return self._async_service

    def _require_base_url(self) -> str:
        """Return the configured base URL, raising when the provider is unconfigured."""
        if self._base_url is None:
            raise MPTError(
                f"{type(self).__name__} must be used with an MPT HTTPClient or AsyncHTTPClient; "
                "the base URL was not configured.",
            )
        return self._base_url

    def _read_expiry(self, token: str) -> dt.datetime | None:
        """Read the ``exp`` claim from the token, ignoring tokens without one."""
        try:
            claims = decode_unverified_jwt_claims(token)
        except (JWTFormatError, JWTClaimsError):
            return None
        exp = claims.get("exp")
        if not isinstance(exp, int):
            return None
        return dt.datetime.fromtimestamp(exp, tz=dt.UTC)
