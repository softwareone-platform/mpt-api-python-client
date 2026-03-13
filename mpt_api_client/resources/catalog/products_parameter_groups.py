from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class ParameterGroup(Model):
    """Parameter Group resource.

    Attributes:
        name: Parameter group name.
        label: Display label for the parameter group.
        description: Parameter group description.
        display_order: Display order of the group.
        default: Whether this is the default parameter group.
        parameter_count: Number of parameters in this group.
        product: Reference to the product this group belongs to.
        audit: Audit information (created, updated events).
    """

    name: str | None
    label: str | None
    description: str | None
    display_order: int | None
    default: bool | None
    parameter_count: int | None
    product: BaseModel | None
    audit: BaseModel | None


class ParameterGroupsServiceConfig:
    """Parameter Groups service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/parameter-groups"
    _model_class = ParameterGroup
    _collection_key = "data"


class ParameterGroupsService(
    ManagedResourceMixin[ParameterGroup],
    CollectionMixin[ParameterGroup],
    Service[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Parameter Groups service."""


class AsyncParameterGroupsService(
    AsyncManagedResourceMixin[ParameterGroup],
    AsyncCollectionMixin[ParameterGroup],
    AsyncService[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Parameter Groups service."""
