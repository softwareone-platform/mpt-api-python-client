from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.price_list_items import (
    AsyncPriceListItemsService,
    PriceListItemsService,
)


class PriceList(Model):
    """Price List resource."""


class PriceListsServiceConfig:
    """Price Lists service configuration."""

    _endpoint = "/public/v1/catalog/price-lists"
    _model_class = PriceList
    _collection_key = "data"


class PriceListsService(
    ManagedResourceMixin[PriceList],
    CollectionMixin[PriceList],
    Service[PriceList],
    PriceListsServiceConfig,
):
    """Price Lists service."""

    def items(self, price_list_id: str) -> PriceListItemsService:
        """Price List Items service."""
        return PriceListItemsService(
            http_client=self.http_client, endpoint_params={"price_list_id": price_list_id}
        )


class AsyncPriceListsService(
    AsyncManagedResourceMixin[PriceList],
    AsyncCollectionMixin[PriceList],
    AsyncService[PriceList],
    PriceListsServiceConfig,
):
    """Price Lists service."""

    def items(self, price_list_id: str) -> AsyncPriceListItemsService:
        """Price List Items service."""
        return AsyncPriceListItemsService(
            http_client=self.http_client, endpoint_params={"price_list_id": price_list_id}
        )
