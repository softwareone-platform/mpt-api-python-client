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
    CreateMixin[Item],
    DeleteMixin,
    GetMixin[Item],
    UpdateMixin[Item],
    PublishableMixin[Item],
    Service[Item],
    ItemsServiceConfig,
):
    """Items service."""


class AsyncItemsService(
    AsyncCreateMixin[Item],
    AsyncDeleteMixin,
    AsyncGetMixin[Item],
    AsyncUpdateMixin[Item],
    AsyncPublishableMixin[Item],
    AsyncService[Item],
    ItemsServiceConfig,
):
    """Items service."""
