from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class ParameterGroupParameter(Model):
    """Helpdesk parameter group parameter resource."""


class ParameterGroupParametersServiceConfig:
    """Helpdesk parameter group parameters service configuration."""

    _endpoint = "/public/v1/helpdesk/parameter-groups/{group_id}/parameters"
    _model_class = ParameterGroupParameter
    _collection_key = "data"


class ParameterGroupParametersService(
    ManagedResourceMixin[ParameterGroupParameter],
    CollectionMixin[ParameterGroupParameter],
    Service[ParameterGroupParameter],
    ParameterGroupParametersServiceConfig,
):
    """Helpdesk parameter group parameters service."""


class AsyncParameterGroupParametersService(
    AsyncManagedResourceMixin[ParameterGroupParameter],
    AsyncCollectionMixin[ParameterGroupParameter],
    AsyncService[ParameterGroupParameter],
    ParameterGroupParametersServiceConfig,
):
    """Async helpdesk parameter group parameters service."""
