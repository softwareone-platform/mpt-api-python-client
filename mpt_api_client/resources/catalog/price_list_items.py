from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class PriceListItem(Model):
    """Price List Item resource."""


class PriceListItemsServiceConfig:
    """Price List Items service configuration."""

    _endpoint = "/public/v1/catalog/price-lists/{price_list_id}/items"
    _model_class = PriceListItem
    _collection_key = "data"


class PriceListItemsService(
    ManagedResourceMixin[PriceListItem],
    CollectionMixin[PriceListItem],
    Service[PriceListItem],
    PriceListItemsServiceConfig,
):
    """Price List Items service."""


class AsyncPriceListItemsService(
    AsyncManagedResourceMixin[PriceListItem],
    AsyncCollectionMixin[PriceListItem],
    AsyncService[PriceListItem],
    PriceListItemsServiceConfig,
):
    """Price List Items service."""
