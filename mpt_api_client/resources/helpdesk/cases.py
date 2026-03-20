from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model, ResourceData


class Case(Model):
    """Helpdesk Case resource."""


class CasesServiceConfig:
    """Helpdesk Cases service configuration."""

    _endpoint = "/public/v1/helpdesk/cases"
    _model_class = Case
    _collection_key = "data"


class CasesService(
    CreateMixin[Case],
    UpdateMixin[Case],
    GetMixin[Case],
    CollectionMixin[Case],
    Service[Case],
    CasesServiceConfig,
):
    """Helpdesk Cases service."""

    def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to query state."""
        return self._resource_action(resource_id, "POST", "query", json=resource_data)

    def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to process state."""
        return self._resource_action(resource_id, "POST", "process", json=resource_data)

    def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to complete state."""
        return self._resource_action(resource_id, "POST", "complete", json=resource_data)


class AsyncCasesService(
    AsyncCreateMixin[Case],
    AsyncUpdateMixin[Case],
    AsyncGetMixin[Case],
    AsyncCollectionMixin[Case],
    AsyncService[Case],
    CasesServiceConfig,
):
    """Async Helpdesk Cases service."""

    async def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to query state."""
        return await self._resource_action(resource_id, "POST", "query", json=resource_data)

    async def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to process state."""
        return await self._resource_action(resource_id, "POST", "process", json=resource_data)

    async def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to complete state."""
        return await self._resource_action(resource_id, "POST", "complete", json=resource_data)
