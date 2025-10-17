from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class Parameter(Model):
    """Parameter resource."""


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
