"""Extension framework authentication for the MPT integration API.

This provider fetches its short-lived token through :class:`InstallationsTokenService`, the
single owner of the installations token endpoint, over a dedicated client authenticated with
the extension secret.
"""

import datetime as dt
from collections.abc import AsyncGenerator, Generator
from typing import override

import httpx

from mpt_api_client.auth.base import Authentication, BearerTokenAuthentication
from mpt_api_client.auth.jwt import JWTClaimsError, JWTFormatError, decode_unverified_jwt_claims
from mpt_api_client.exceptions import MPTError
from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.integration.installations_token import (
    AsyncInstallationsTokenService,
    InstallationsTokenService,
)

DEFAULT_TOKEN_VALIDITY_LEEWAY_SECONDS = 60


class ExtensionFrameworkAuthentication(Authentication):
    """Authenticate with a short-lived installation or account-scoped token.

    The token is fetched through the installations token service using the extension secret
    and cached. When ``account_id`` is provided, the token is scoped to that account.
    Refresh happens proactively once the token is within ``min_remaining_validity_seconds``
    of its JWT ``exp`` claim, with a reactive refresh on ``401 Unauthorized`` as a fallback
    for tokens revoked before they expire. When the fetched token carries no readable
    ``exp`` claim, proactive refresh is skipped and only the reactive ``401`` path applies.

    The token call is delegated to :class:`InstallationsTokenService` (and its async
    counterpart) over a dedicated client authenticated with the extension secret; that
    client's base URL is supplied by the owning HTTP client through :meth:`configure`. Each
    provider instance caches a single token for its own scope, so callers needing several
    account scopes should construct one provider per scope.
    """

    def __init__(
        self,
        secret: str,
        account_id: str | None = None,
        min_remaining_validity_seconds: int = DEFAULT_TOKEN_VALIDITY_LEEWAY_SECONDS,
    ) -> None:
        """Initialize the provider.

        Args:
            secret: Extension secret used to authenticate token requests.
            account_id: When set, request a token scoped to this account.
            min_remaining_validity_seconds: Proactive refresh leeway before the JWT ``exp``.
        """
        self._secret = secret
        self._account_id = account_id
        self._min_remaining_validity_seconds = min_remaining_validity_seconds
        self._token: str | None = None
        self._expires_at: dt.datetime | None = None
        self._base_url: str | None = None
        self._timeout: float = 20.0
        self._retries: int = 5
        self._sync_service: InstallationsTokenService | None = None
        self._async_service: AsyncInstallationsTokenService | None = None

    @override
    def configure(self, *, base_url: str, timeout: float, retries: int) -> None:
        """Store the owning client's configuration used to build the token client."""
        self._base_url = base_url
        self._timeout = timeout
        self._retries = retries

    @override
    def sync_auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Attach a cached token, refreshing it proactively and on 401."""
        if self._token is None or self._is_expired():
            self._refresh_sync()
        request.headers["Authorization"] = f"Bearer {self._token}"
        response = yield request
        if response.status_code == httpx.codes.UNAUTHORIZED:
            self._refresh_sync()
            request.headers["Authorization"] = f"Bearer {self._token}"
            yield request

    @override
    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        """Attach a cached token, refreshing it proactively and on 401."""
        if self._token is None or self._is_expired():
            await self._refresh_async()
        request.headers["Authorization"] = f"Bearer {self._token}"
        response = yield request
        if response.status_code == httpx.codes.UNAUTHORIZED:
            await self._refresh_async()
            request.headers["Authorization"] = f"Bearer {self._token}"
            yield request

    def _refresh_sync(self) -> None:
        """Fetch and cache a fresh token via the sync installations token service."""
        token = self._get_sync_service().token(self._account_id)
        self._store(token.token)

    async def _refresh_async(self) -> None:
        """Fetch and cache a fresh token via the async installations token service."""
        token = await self._get_async_service().token(self._account_id)
        self._store(token.token)

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
                "ExtensionFrameworkAuthentication must be used with an MPT HTTPClient or "
                "AsyncHTTPClient; the base URL was not configured.",
            )
        return self._base_url

    def _store(self, token: str | None) -> None:
        """Cache a freshly fetched token and its expiry."""
        if not token:
            raise MPTError("Installations token endpoint returned an empty token.")
        self._token = token
        self._expires_at = self._read_expiry(token)

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

    def _is_expired(self) -> bool:
        """Return whether the cached token is within the refresh leeway of expiry."""
        if self._expires_at is None:
            return False
        threshold = dt.datetime.now(dt.UTC).timestamp() + self._min_remaining_validity_seconds
        return self._expires_at.timestamp() <= threshold
