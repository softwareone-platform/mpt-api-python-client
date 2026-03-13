from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class Item(Model):  # noqa: WPS110
    """Item resource.

    Attributes:
        name: Item name.
        description: Item description.
        external_ids: External identifiers for the item.
        group: Reference to the item group.
        unit: Reference to the unit of measure.
        terms: Reference to the terms and conditions.
        quantity_not_applicable: Whether quantity is not applicable to this item.
        status: Item status.
        product: Reference to the product.
        parameters: List of parameters associated with this item.
        audit: Audit information (created, updated events).
    """

    name: str | None
    description: str | None
    external_ids: BaseModel | None
    group: BaseModel | None
    unit: BaseModel | None
    terms: BaseModel | None
    quantity_not_applicable: bool | None
    status: str | None
    product: BaseModel | None
    parameters: list[BaseModel] | None
    audit: BaseModel | None


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
