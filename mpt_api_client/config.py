"""Client configuration shared between the HTTP clients and authentication providers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientConfig:
    """Configuration of an MPT HTTP client.

    ``base_url=None`` means "not set"; the owning client falls back to the
    ``MPT_API_BASE_URL`` environment variable after the authentication provider
    had a chance to amend the configuration.
    """

    base_url: str | None = None
    timeout: float = 20.0
    retries: int = 5
