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


class ParameterGroup(Model):
    """Parameter Group resource."""


class ParameterGroupsServiceConfig:
    """Parameter Groups service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/parameter-groups"
    _model_class = ParameterGroup
    _collection_key = "data"


class ParameterGroupsService(
    CreateMixin[ParameterGroup],
    DeleteMixin,
    GetMixin[ParameterGroup],
    UpdateMixin[ParameterGroup],
    Service[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Parameter Groups service."""


class AsyncParameterGroupsService(
    AsyncCreateMixin[ParameterGroup],
    AsyncDeleteMixin,
    AsyncGetMixin[ParameterGroup],
    AsyncUpdateMixin[ParameterGroup],
    AsyncService[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Parameter Groups service."""
