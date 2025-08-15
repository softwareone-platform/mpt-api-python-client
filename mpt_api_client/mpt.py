from mpt_api_client.http.client import MPTClient


class MPT:
    """MPT API Client."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.mpt_client = MPTClient(base_url=base_url, api_token=api_key)
