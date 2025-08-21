import os

from httpx import AsyncClient, AsyncHTTPTransport, Client, HTTPTransport


class HTTPClient(Client):
    """Sync HTTP client for interacting with SoftwareOne Marketplace Platform API."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_token: str | None = None,
        timeout: float = 5.0,
        retries: int = 0,
    ):
        api_token = api_token or os.getenv("MPT_TOKEN")
        if not api_token:
            raise ValueError(
                "API token is required. "
                "Set it up as env variable MPT_TOKEN or pass it as `api_token` "
                "argument to MPTClient."
            )

        base_url = base_url or os.getenv("MPT_URL")
        if not base_url:
            raise ValueError(
                "Base URL is required. "
                "Set it up as env variable MPT_URL or pass it as `base_url` "
                "argument to MPTClient."
            )
        base_headers = {
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": f"Bearer {api_token}",
        }
        Client.__init__(
            self,
            base_url=base_url,
            headers=base_headers,
            timeout=timeout,
            transport=HTTPTransport(retries=retries),
        )


class HTTPClientAsync(AsyncClient):
    """Async HTTP client for interacting with SoftwareOne Marketplace Platform API."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_token: str | None = None,
        timeout: float = 5.0,
        retries: int = 0,
    ):
        api_token = api_token or os.getenv("MPT_TOKEN")
        if not api_token:
            raise ValueError(
                "API token is required. "
                "Set it up as env variable MPT_TOKEN or pass it as `api_token` "
                "argument to MPTClient."
            )

        base_url = base_url or os.getenv("MPT_URL")
        if not base_url:
            raise ValueError(
                "Base URL is required. "
                "Set it up as env variable MPT_URL or pass it as `base_url` "
                "argument to MPTClient."
            )
        base_headers = {
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": f"Bearer {api_token}",
        }
        AsyncClient.__init__(
            self,
            base_url=base_url,
            headers=base_headers,
            timeout=timeout,
            transport=AsyncHTTPTransport(retries=retries),
        )
