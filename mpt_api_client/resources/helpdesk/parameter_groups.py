from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.helpdesk.parameter_group_parameters import (
    AsyncParameterGroupParametersService,
    ParameterGroupParametersService,
)


class ParameterGroup(Model):
    """Helpdesk parameter group resource."""


class ParameterGroupsServiceConfig:
    """Helpdesk parameter groups service configuration."""

    _endpoint = "/public/v1/helpdesk/parameter-groups"
    _model_class = ParameterGroup
    _collection_key = "data"


class ParameterGroupsService(
    ManagedResourceMixin[ParameterGroup],
    CollectionMixin[ParameterGroup],
    Service[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Helpdesk parameter groups service."""

    def parameters(self, group_id: str) -> ParameterGroupParametersService:  # noqa: WPS110
        """Return parameter group parameters service."""
        return ParameterGroupParametersService(
            http_client=self.http_client, endpoint_params={"group_id": group_id}
        )


class AsyncParameterGroupsService(
    AsyncManagedResourceMixin[ParameterGroup],
    AsyncCollectionMixin[ParameterGroup],
    AsyncService[ParameterGroup],
    ParameterGroupsServiceConfig,
):
    """Async helpdesk parameter groups service."""

    def parameters(self, group_id: str) -> AsyncParameterGroupParametersService:  # noqa: WPS110
        """Return async parameter group parameters service."""
        return AsyncParameterGroupParametersService(
            http_client=self.http_client, endpoint_params={"group_id": group_id}
        )
