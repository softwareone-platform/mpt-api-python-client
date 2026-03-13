from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Parameter(Model):
    """Parameter resource.

    Attributes:
        name: Parameter name.
        description: Parameter description.
        scope: Parameter scope (e.g. Agreement, Item, Request, Subscription, Order, Asset).
        phase: Parameter phase (e.g. Configuration, Order, Fulfillment).
        context: Parameter context (e.g. None, Purchase, Change, Configuration, Termination).
        type: Parameter type (e.g. SingleLineText, MultiLineText, Address, etc.).
        status: Parameter status.
        external_id: External identifier for the parameter.
        display_order: Display order of the parameter.
        group: Reference to the parameter group.
        product: Reference to the product this parameter belongs to.
        constraints: Parameter constraints (required, hidden, readonly).
        audit: Audit information (created, updated events).
        options: Type-specific parameter options.
    """

    name: str | None
    description: str | None
    scope: str | None
    phase: str | None
    context: str | None
    type: str | None
    status: str | None
    external_id: str | None
    display_order: int | None
    group: BaseModel | None
    product: BaseModel | None
    constraints: BaseModel | None
    audit: BaseModel | None
    options: BaseModel | None


class ParametersServiceConfig:
    """Parameters service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/parameters"
    _model_class = Parameter
    _collection_key = "data"


class ParametersService(
    ManagedResourceMixin[Parameter],
    CollectionMixin[Parameter],
    Service[Parameter],
    ParametersServiceConfig,
):
    """Parameters service."""


class AsyncParametersService(
    AsyncManagedResourceMixin[Parameter],
    AsyncCollectionMixin[Parameter],
    AsyncService[Parameter],
    ParametersServiceConfig,
):
    """Parameters service."""
