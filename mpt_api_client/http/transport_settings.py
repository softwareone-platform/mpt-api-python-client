import os
from dataclasses import dataclass
from typing import cast, override

from httpx import Timeout
from httpx_retries import Retry

from mpt_api_client.http.client_utils import validate_base_url

RETRY_ALLOWED_METHODS = frozenset(("DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH"))
ENV_BASE_URL = "MPT_API_BASE_URL"
DEFAULT_TIMEOUT = 20.0
DEFAULT_STREAM_READ_TIMEOUT = 120.0


@dataclass
class TransportSettings:
    """Transport-level settings shared by the HTTP clients and auth providers.

    Attributes:
        base_url: Base URL of the MPT API; validated and sanitized at construction
            time. Use ``EnvTransportSettings`` to resolve it from the environment
            instead of passing it explicitly.
        timeout: Default timeout in seconds applied to every connection phase that
            does not set its own value.
        connect_timeout: Timeout for establishing the connection. Falls back to
            ``timeout``.
        read_timeout: Timeout for a single socket read, which includes waiting for the
            response status line. Falls back to ``timeout``.
        write_timeout: Timeout for a single socket write. Falls back to ``timeout``.
        pool_timeout: Timeout for acquiring a connection from the pool. Falls back to
            ``timeout``.
        stream_read_timeout: Read timeout for streaming requests. A streaming request's
            read phase is bounded by the larger of this and ``read_timeout``, so raising
            ``read_timeout`` raises the streaming budget too. Streaming responses commit
            their status only after the server has built the result set, so the first byte
            can be deferred far longer than a regular response; the default covers that
            wait with headroom.
        retries: Retry policy; either the number of retries for failed requests or a
            fully configured ``httpx_retries.Retry`` instance used as is. Normalized
            to a ``Retry`` instance at construction time.

    No total-duration timeout is applied. A streamed export runs for as long as the
    server keeps sending, bounded per phase rather than overall.
    """

    base_url: str | None = None
    timeout: float = DEFAULT_TIMEOUT
    connect_timeout: float | None = None
    read_timeout: float | None = None
    write_timeout: float | None = None
    pool_timeout: float | None = None
    stream_read_timeout: float = DEFAULT_STREAM_READ_TIMEOUT
    retries: int | Retry = 5

    def __post_init__(self) -> None:
        """Validate ``base_url`` and normalize ``retries``.

        Raises:
            ValueError: If ``base_url`` is missing or not a valid URL.
        """
        self.base_url = validate_base_url(self.base_url)
        self.retries = self._build_retry()

    @property
    def url(self) -> str:
        """Validated base URL."""
        return cast("str", self.base_url)

    @property
    def retry(self) -> Retry:
        """Normalized retry policy."""
        return cast("Retry", self.retries)

    @property
    def request_timeout(self) -> Timeout:
        """Per-phase timeout for regular requests."""
        return Timeout(
            connect=self._phase_timeout(self.connect_timeout),
            read=self._phase_timeout(self.read_timeout),
            write=self._phase_timeout(self.write_timeout),
            pool=self._phase_timeout(self.pool_timeout),
        )

    @property
    def stream_timeout(self) -> Timeout:
        """Per-phase timeout for streaming requests, with a longer read timeout."""
        return Timeout(
            connect=self._phase_timeout(self.connect_timeout),
            read=max(self.stream_read_timeout, self._phase_timeout(self.read_timeout)),
            write=self._phase_timeout(self.write_timeout),
            pool=self._phase_timeout(self.pool_timeout),
        )

    def _phase_timeout(self, phase_value: float | None) -> float:
        """Return the phase timeout, falling back to the default timeout when unset."""
        return self.timeout if phase_value is None else phase_value

    def _build_retry(self) -> Retry:
        """Return the retry policy, building one when ``retries`` is a plain count."""
        if isinstance(self.retries, Retry):
            return self.retries
        return Retry(total=self.retries, allowed_methods=set(RETRY_ALLOWED_METHODS))


@dataclass
class EnvTransportSettings(TransportSettings):
    """Transport settings that read the base URL from the environment.

    When ``base_url`` is not provided explicitly, it is resolved from the
    ``MPT_API_BASE_URL`` environment variable at construction time.
    """

    @override
    def __post_init__(self) -> None:
        """Resolve ``base_url`` from the environment, then validate and normalize.

        Raises:
            ValueError: If no base URL is provided and the environment variable is
                not set, or the resolved URL is invalid.
        """
        if self.base_url is None:
            self.base_url = os.getenv(ENV_BASE_URL)
        super().__post_init__()
