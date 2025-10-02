from typing import Self

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources import (
    Accounts,
    AsyncAccounts,
    AsyncAudit,
    AsyncBilling,
    AsyncCatalog,
    AsyncCommerce,
    AsyncNotifications,
    Audit,
    Billing,
    Catalog,
    Commerce,
    Notifications,
)


class AsyncMPTClient:
    """MPT API Client."""

    def __init__(
        self,
        http_client: AsyncHTTPClient | None = None,
    ):
        self.http_client = http_client or AsyncHTTPClient()

    @classmethod
    def from_config(cls, api_token: str, base_url: str) -> Self:
        """Create MPT client from configuration.

        Args:
            api_token: MPT API Token
            base_url: MPT Base URL

        Returns:
            MPT Client

        """
        return cls(AsyncHTTPClient(base_url=base_url, api_token=api_token))

    @property
    def catalog(self) -> AsyncCatalog:
        """Catalog MPT API Client."""
        return AsyncCatalog(http_client=self.http_client)

    @property
    def commerce(self) -> AsyncCommerce:
        """Commerce MPT API Client."""
        return AsyncCommerce(http_client=self.http_client)

    @property
    def audit(self) -> AsyncAudit:
        """Audit MPT API Client."""
        return AsyncAudit(http_client=self.http_client)

    @property
    def billing(self) -> AsyncBilling:
        """Billing MPT API Client."""
        return AsyncBilling(http_client=self.http_client)

    @property
    def accounts(self) -> AsyncAccounts:
        """Accounts MPT API Client."""
        return AsyncAccounts(http_client=self.http_client)

    @property
    def notifications(self) -> AsyncNotifications:
        """Notifications MPT API Client."""
        return AsyncNotifications(http_client=self.http_client)


class MPTClient:
    """MPT API Client."""

    def __init__(
        self,
        http_client: HTTPClient | None = None,
    ):
        self.http_client = http_client or HTTPClient()

    @classmethod
    def from_config(cls, api_token: str, base_url: str) -> Self:
        """Create MPT client from configuration.

        Args:
            api_token: MPT API Token
            base_url: MPT Base URL

        Returns:
            MPT Client

        """
        return cls(HTTPClient(base_url=base_url, api_token=api_token))

    @property
    def commerce(self) -> Commerce:
        """Commerce MPT API Client.

        The Commerce API provides a comprehensive set of endpoints
        for managing agreements, requests, subscriptions, and orders
        within a vendor-client-ops ecosystem.
        """
        return Commerce(http_client=self.http_client)

    @property
    def catalog(self) -> Catalog:
        """Catalog MPT API Client."""
        return Catalog(http_client=self.http_client)

    @property
    def audit(self) -> Audit:
        """Audit MPT API Client."""
        return Audit(http_client=self.http_client)

    @property
    def billing(self) -> Billing:
        """Billing MPT API Client."""
        return Billing(http_client=self.http_client)

    @property
    def accounts(self) -> Accounts:
        """Accounts MPT API Client."""
        return Accounts(http_client=self.http_client)

    @property
    def notifications(self) -> Notifications:
        """Notifications MPT API Client."""
        return Notifications(http_client=self.http_client)
