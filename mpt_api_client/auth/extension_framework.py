"""Extension framework authentication for the MPT integration API.

This provider fetches its short-lived token through :class:`InstallationsTokenService`, the
single owner of the installations token endpoint, over a dedicated client authenticated with
the extension secret.
"""

import datetime as dt
from collections.abc import AsyncGenerator, Generator
from typing import override

import httpx

from mpt_api_client.auth.base import InstallationTokenAuthentication
from mpt_api_client.exceptions import MPTError

DEFAULT_TOKEN_VALIDITY_LEEWAY_SECONDS = 60


class ExtensionFrameworkAuthentication(InstallationTokenAuthentication):
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
        super().__init__(secret)
        self._account_id = account_id
        self._min_remaining_validity_seconds = min_remaining_validity_seconds
        self._token: str | None = None
        self._expires_at: dt.datetime | None = None

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

    def _store(self, token: str | None) -> None:
        """Cache a freshly fetched token and its expiry."""
        if not token:
            raise MPTError("Installations token endpoint returned an empty token.")
        self._token = token
        self._expires_at = self._read_expiry(token)

    def _is_expired(self) -> bool:
        """Return whether the cached token is within the refresh leeway of expiry."""
        if self._expires_at is None:
            return False
        threshold = dt.datetime.now(dt.UTC).timestamp() + self._min_remaining_validity_seconds
        return self._expires_at.timestamp() <= threshold
