from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.commerce.agreements import AgreementsService, AsyncAgreementsService
from mpt_api_client.resources.commerce.assets import AssetService, AsyncAssetService
from mpt_api_client.resources.commerce.orders import AsyncOrdersService, OrdersService
from mpt_api_client.resources.commerce.subscriptions import (
    AsyncSubscriptionsService,
    SubscriptionsService,
)


class Commerce:
    """Commerce MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def agreements(self) -> AgreementsService:
        """Agreement service."""
        return AgreementsService(http_client=self.http_client)

    @property
    def orders(self) -> OrdersService:
        """Order service."""
        return OrdersService(http_client=self.http_client)

    @property
    def subscriptions(self) -> SubscriptionsService:
        """Subscription service."""
        return SubscriptionsService(http_client=self.http_client)

    @property
    def assets(self) -> AssetService:
        """Asset service."""
        return AssetService(http_client=self.http_client)


class AsyncCommerce:
    """Commerce MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def agreements(self) -> AsyncAgreementsService:
        """Agreement service."""
        return AsyncAgreementsService(http_client=self.http_client)

    @property
    def orders(self) -> AsyncOrdersService:
        """Order service."""
        return AsyncOrdersService(http_client=self.http_client)

    @property
    def subscriptions(self) -> AsyncSubscriptionsService:
        """Subscription service."""
        return AsyncSubscriptionsService(http_client=self.http_client)

    @property
    def assets(self) -> AsyncAssetService:
        """Asset service."""
        return AsyncAssetService(http_client=self.http_client)
