import httpx


class MPTClient(httpx.Client):
    """A client for interacting with SoftwareOne Marketplace Platform API."""

    def __init__(
        self,
        *,
        base_url: str,
        api_token: str,
        timeout: float = 5.0,
        retries: int = 0,
    ):
        self.api_token = api_token
        base_headers = {
            "User-Agent": "swo-marketplace-client/1.0",
            "Authorization": f"Bearer {api_token}",
        }
        super().__init__(
            base_url=base_url,
            headers=base_headers,
            timeout=timeout,
            transport=httpx.HTTPTransport(retries=retries),
        )
