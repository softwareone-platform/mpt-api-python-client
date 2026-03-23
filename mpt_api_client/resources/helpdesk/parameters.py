from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class Parameter(Model):
    """Helpdesk parameter definition resource."""


class ParametersServiceConfig:
    """Helpdesk parameters service configuration."""

    _endpoint = "/public/v1/helpdesk/parameters"
    _model_class = Parameter
    _collection_key = "data"


class ParametersService(
    ManagedResourceMixin[Parameter],
    CollectionMixin[Parameter],
    Service[Parameter],
    ParametersServiceConfig,
):
    """Helpdesk parameters service."""


class AsyncParametersService(
    AsyncManagedResourceMixin[Parameter],
    AsyncCollectionMixin[Parameter],
    AsyncService[Parameter],
    ParametersServiceConfig,
):
    """Async helpdesk parameters service."""
