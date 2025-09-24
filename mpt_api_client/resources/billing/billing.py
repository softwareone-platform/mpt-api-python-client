from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.billing.journals import AsyncJournalsService, JournalsService


class Billing:
    """Billing MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def journals(self) -> JournalsService:
        """Journals service."""
        return JournalsService(http_client=self.http_client)


class AsyncBilling:
    """Billing MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def journals(self) -> AsyncJournalsService:
        """Journals service."""
        return AsyncJournalsService(http_client=self.http_client)
