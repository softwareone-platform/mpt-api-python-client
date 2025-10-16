from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    UpdateMixin,
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
    CreateMixin[ItemGroup],
    DeleteMixin,
    GetMixin[ItemGroup],
    UpdateMixin[ItemGroup],
    Service[ItemGroup],
    ItemGroupsServiceConfig,
):
    """Item Groups service."""


class AsyncItemGroupsService(
    AsyncCreateMixin[ItemGroup],
    AsyncDeleteMixin,
    AsyncGetMixin[ItemGroup],
    AsyncUpdateMixin[ItemGroup],
    AsyncService[ItemGroup],
    ItemGroupsServiceConfig,
):
    """Item Groups service."""
