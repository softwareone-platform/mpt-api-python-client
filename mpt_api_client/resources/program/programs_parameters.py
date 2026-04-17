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
        scope: Parameter scope.
        phase: Parameter phase (e.g. Order, Fulfillment).
        program: Reference to the program this parameter belongs to.
        description: Parameter description.
        multiple: Whether multiple values are allowed for this parameter.
        external_id: External identifier for the parameter.
        display_order: Display order of the parameter.
        constraints: Parameter constraints (required, hidden, readonly).
        options: Type-specific parameter options.
        type: Parameter type (e.g. SingleLineText, MultiLineText, Address, etc.).
        status: Parameter status.
        audit: Audit information (created, updated events).
    """

    name: str | None
    scope: str | None
    phase: str | None
    program: BaseModel | None
    description: str | None
    multiple: bool | None
    external_id: str | None
    display_order: int | None
    constraints: BaseModel | None
    options: BaseModel | None
    type: str | None
    status: str | None
    audit: BaseModel | None


class ParametersServiceConfig:
    """Parameters service configuration."""

    _endpoint = "/public/v1/program/programs/{program_id}/parameters"
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
