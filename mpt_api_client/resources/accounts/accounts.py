from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.accounts.account import AccountsService, AsyncAccountsService


class Accounts:
    """Accounts MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def accounts(self) -> AccountsService:
        """Accounts service."""
        return AccountsService(http_client=self.http_client)


class AsyncAccounts:
    """Async Accounts MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def accounts(self) -> AsyncAccountsService:
        """Accounts service."""
        return AsyncAccountsService(http_client=self.http_client)
