from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.resources.catalog.items import Item


class ProductItemServiceConfig:
    """Product Item service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/items"
    _model_class = Item
    _collection_key = "data"


class ProductItemService(
    GetMixin[Item],
    CollectionMixin[Item],
    Service[Item],
    ProductItemServiceConfig,
):
    """Product Item service."""


class AsyncProductItemService(
    AsyncGetMixin[Item],
    AsyncCollectionMixin[Item],
    AsyncService[Item],
    ProductItemServiceConfig,
):
    """Product Item service."""
