from mpt_api_client.http import AsyncService, CreateMixin, DeleteMixin, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
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
    UpdateMixin[ParameterGroup],
    Service[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Parameter Groups service."""


class AsyncParameterGroupsService(
    AsyncCreateMixin[ParameterGroup],
    AsyncDeleteMixin,
    AsyncUpdateMixin[ParameterGroup],
    AsyncService[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Parameter Groups service."""
