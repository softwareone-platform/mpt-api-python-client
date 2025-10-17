from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class ItemGroup(Model):
    """Item Group resource."""


class ItemGroupsServiceConfig:
    """Item Groups service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/item-groups"
    _model_class = ItemGroup
    _collection_key = "data"


class ItemGroupsService(
    ManagedResourceMixin[ItemGroup],
    CollectionMixin[ItemGroup],
    Service[ItemGroup],
    ItemGroupsServiceConfig,
):
    """Item Groups service."""


class AsyncItemGroupsService(
    AsyncManagedResourceMixin[ItemGroup],
    AsyncCollectionMixin[ItemGroup],
    AsyncService[ItemGroup],
    ItemGroupsServiceConfig,
):
    """Item Groups service."""
