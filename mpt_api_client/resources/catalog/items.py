from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class Item(Model):  # noqa: WPS110
    """Item resource."""


class ItemsServiceConfig:
    """Items service configuration."""

    _endpoint = "/public/v1/catalog/items"
    _model_class = Item
    _collection_key = "data"


class ItemsService(
    PublishableMixin[Item],
    ManagedResourceMixin[Item],
    CollectionMixin[Item],
    Service[Item],
    ItemsServiceConfig,
):
    """Items service."""


class AsyncItemsService(
    AsyncPublishableMixin[Item],
    AsyncManagedResourceMixin[Item],
    AsyncCollectionMixin[Item],
    AsyncService[Item],
    ItemsServiceConfig,
):
    """Items service."""
