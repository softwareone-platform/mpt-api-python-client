import os
from dataclasses import dataclass
from typing import cast, override

from httpx_retries import Retry

from mpt_api_client.http.client_utils import validate_base_url

RETRY_ALLOWED_METHODS = frozenset(("DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH"))
ENV_BASE_URL = "MPT_API_BASE_URL"


@dataclass
class TransportSettings:
    """Transport-level settings shared by the HTTP clients and auth providers.

    Attributes:
        base_url: Base URL of the MPT API; validated and sanitized at construction
            time. Use ``EnvTransportSettings`` to resolve it from the environment
            instead of passing it explicitly.
        timeout: HTTP request timeout in seconds.
        retries: Retry policy; either the number of retries for failed requests or a
            fully configured ``httpx_retries.Retry`` instance used as is. Normalized
            to a ``Retry`` instance at construction time.
    """

    base_url: str | None = None
    timeout: float = 20.0
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
