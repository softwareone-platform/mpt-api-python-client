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


class Parameter(Model):
    """Parameter resource."""


class ParametersServiceConfig:
    """Parameters service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/parameters"
    _model_class = Parameter
    _collection_key = "data"


class ParametersService(
    CreateMixin[Parameter],
    DeleteMixin,
    GetMixin[Parameter],
    UpdateMixin[Parameter],
    Service[Parameter],
    ParametersServiceConfig,
):
    """Parameters service."""


class AsyncParametersService(
    AsyncCreateMixin[Parameter],
    AsyncDeleteMixin,
    AsyncGetMixin[Parameter],
    AsyncUpdateMixin[Parameter],
    AsyncService[Parameter],
    ParametersServiceConfig,
):
    """Parameters service."""
