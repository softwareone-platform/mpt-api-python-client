from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, CasesService


class Helpdesk:
    """Helpdesk MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def cases(self) -> CasesService:
        """Cases service."""
        return CasesService(http_client=self.http_client)


class AsyncHelpdesk:
    """Async Helpdesk MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def cases(self) -> AsyncCasesService:
        """Cases service."""
        return AsyncCasesService(http_client=self.http_client)
