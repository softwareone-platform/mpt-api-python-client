"""Account-scoped authentication for the MPT integration API.

This provider fetches account-scoped installation tokens and shares them across instances
through a process-wide cache keyed by ``(secret, account_id)``. Token fetches are serialized
per account, so concurrent callers for the same account trigger at most one token request.
"""

import asyncio
import datetime as dt
import threading
from collections.abc import AsyncGenerator, Generator
from dataclasses import dataclass
from typing import ClassVar, override

import httpx

from mpt_api_client.auth.base import InstallationTokenAuthentication
from mpt_api_client.exceptions import MPTError

DEFAULT_TOKEN_VALIDITY_LEEWAY_SECONDS = 60

CacheKey = tuple[str, str]


@dataclass(frozen=True)
class _CachedToken:
    """A cached account token together with its decoded expiry."""

    token: str
    expires_at: dt.datetime | None


class AccountScopedAuthentication(InstallationTokenAuthentication):  # noqa: WPS214
    """Authenticate with an account-scoped token from a shared, concurrency-safe cache.

    Tokens are cached process-wide keyed by ``(secret, account_id)``, so several provider or
    client instances for the same account reuse a single token. Refresh is serialized per
    account through a lock with double-checked caching: concurrent callers for the same
    account trigger at most one token request. Refresh happens proactively once the token is
    within ``min_remaining_validity_seconds`` of its JWT ``exp`` claim, with a reactive
    refresh on ``401 Unauthorized`` for tokens revoked before they expire. When the fetched
    token carries no readable ``exp`` claim, proactive refresh is skipped and only the
    reactive ``401`` path applies.

    The token call is delegated to :class:`InstallationsTokenService` (and its async
    counterpart) over a dedicated client authenticated with the extension secret; that
    client's base URL is supplied by the owning HTTP client through :meth:`configure`.
    """

    _token_cache: ClassVar[dict[CacheKey, _CachedToken]] = {}
    _sync_locks: ClassVar[dict[CacheKey, threading.Lock]] = {}
    _async_locks: ClassVar[dict[CacheKey, asyncio.Lock]] = {}

    def __init__(
        self,
        secret: str,
        account_id: str,
        min_remaining_validity_seconds: int = DEFAULT_TOKEN_VALIDITY_LEEWAY_SECONDS,
    ) -> None:
        """Initialize the provider.

        Args:
            secret: Extension secret used to authenticate token requests.
            account_id: Account the requested token is scoped to.
            min_remaining_validity_seconds: Proactive refresh leeway before the JWT ``exp``.
        """
        super().__init__(secret)
        self._account_id = account_id
        self._min_remaining_validity_seconds = min_remaining_validity_seconds

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all cached account tokens and refresh locks."""
        cls._token_cache.clear()
        cls._sync_locks.clear()
        cls._async_locks.clear()

    @override
    def sync_auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Attach an account-scoped token, refreshing it proactively and on 401."""
        token = self._token_sync()
        request.headers["Authorization"] = f"Bearer {token}"
        response = yield request
        if response.status_code == httpx.codes.UNAUTHORIZED:
            rejected = request.headers["Authorization"].removeprefix("Bearer ")
            request.headers["Authorization"] = f"Bearer {self._token_sync(rejected)}"
            yield request

    @override
    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        """Attach an account-scoped token, refreshing it proactively and on 401."""
        token = await self._token_async()
        request.headers["Authorization"] = f"Bearer {token}"
        response = yield request
        if response.status_code == httpx.codes.UNAUTHORIZED:
            rejected = request.headers["Authorization"].removeprefix("Bearer ")
            refreshed = await self._token_async(rejected)
            request.headers["Authorization"] = f"Bearer {refreshed}"
            yield request

    @property
    def _cache_key(self) -> CacheKey:
        """Return the shared-cache key for this provider's scope."""
        return self._secret, self._account_id

    def _token_sync(self, rejected: str | None = None) -> str:
        """Return a usable token, fetching one under a per-account lock when needed."""
        cached = self._token_cache.get(self._cache_key)
        if self._is_usable(cached, rejected):
            return cached.token  # type: ignore[union-attr]

        lock = self._sync_locks.setdefault(self._cache_key, threading.Lock())
        with lock:
            cached = self._token_cache.get(self._cache_key)
            if self._is_usable(cached, rejected):
                return cached.token  # type: ignore[union-attr]
            fetched = self._get_sync_service().token(self._account_id)
            return self._store(fetched.token)

    async def _token_async(self, rejected: str | None = None) -> str:
        """Return a usable token, fetching one under a per-account lock when needed."""
        cached = self._token_cache.get(self._cache_key)
        if self._is_usable(cached, rejected):
            return cached.token  # type: ignore[union-attr]

        lock = self._async_locks.setdefault(self._cache_key, asyncio.Lock())
        async with lock:
            cached = self._token_cache.get(self._cache_key)
            if self._is_usable(cached, rejected):
                return cached.token  # type: ignore[union-attr]
            fetched = await self._get_async_service().token(self._account_id)
            return self._store(fetched.token)

    def _is_usable(self, cached: _CachedToken | None, rejected: str | None) -> bool:
        """Return whether the cached token can be reused for the current request.

        A token is unusable when it is missing, when it equals a token the server just
        rejected, or when it is within the proactive refresh leeway of its expiry. Tokens
        without a readable ``exp`` are reused and rely on the reactive ``401`` path.
        """
        if cached is None or cached.token == rejected:
            return False
        if cached.expires_at is None:
            return True
        threshold = dt.datetime.now(dt.UTC).timestamp() + self._min_remaining_validity_seconds
        return cached.expires_at.timestamp() > threshold

    def _store(self, token: str | None) -> str:
        """Cache a freshly fetched token, evicting expired entries, and return it."""
        if not token:
            raise MPTError("Installations token endpoint returned an empty token.")
        self._token_cache[self._cache_key] = _CachedToken(token, self._read_expiry(token))
        self._evict_expired()
        return token

    def _evict_expired(self) -> None:
        """Drop cache entries (and their locks) whose tokens have already expired."""
        now = dt.datetime.now(dt.UTC)
        expired_keys = [
            key
            for key, cached in self._token_cache.items()
            if cached.expires_at is not None and cached.expires_at <= now
        ]
        for key in expired_keys:
            self._token_cache.pop(key, None)
            self._sync_locks.pop(key, None)
            self._async_locks.pop(key, None)
