from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.accounts.account import AccountsService, AsyncAccountsService
from mpt_api_client.resources.accounts.api_tokens import ApiTokensService, AsyncApiTokensService


class Accounts:
    """Accounts MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def accounts(self) -> AccountsService:
        """Accounts service."""
        return AccountsService(http_client=self.http_client)

    @property
    def api_tokens(self) -> ApiTokensService:
        """API Tokens service."""
        return ApiTokensService(http_client=self.http_client)


class AsyncAccounts:
    """Async Accounts MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def accounts(self) -> AsyncAccountsService:
        """Accounts service."""
        return AsyncAccountsService(http_client=self.http_client)

    @property
    def api_tokens(self) -> AsyncApiTokensService:
        """API Tokens service."""
        return AsyncApiTokensService(http_client=self.http_client)
