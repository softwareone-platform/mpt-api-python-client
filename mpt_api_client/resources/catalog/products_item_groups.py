from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class ItemGroup(Model):
    """Item Group resource.

    Attributes:
        name: Item group name.
        label: Display label for the item group.
        description: Item group description.
        display_order: Display order of the group.
        default: Whether this is the default item group.
        multiple: Whether multiple items can be selected from this group.
        required: Whether a selection from this group is required.
        item_count: Number of items in this group.
        product: Reference to the product.
        audit: Audit information (created, updated events).
    """

    name: str | None
    label: str | None
    description: str | None
    display_order: int | None
    default: bool | None
    multiple: bool | None
    required: bool | None
    item_count: int | None
    product: BaseModel | None
    audit: BaseModel | None


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
