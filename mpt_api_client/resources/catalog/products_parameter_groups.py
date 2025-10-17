from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
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
