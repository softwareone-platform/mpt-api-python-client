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
    """Helpdesk case resource."""


class CasesServiceConfig:
    """Cases service configuration."""

    _endpoint = "/public/v1/helpdesk/cases"
    _model_class = Case
    _collection_key = "data"


class CasesService(
    CollectionMixin[Case],
    CreateMixin[Case],
    GetMixin[Case],
    UpdateMixin[Case],
    Service[Case],
    CasesServiceConfig,
):
    """Cases service."""

    def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to complete state.

        Args:
            resource_id: Case resource ID
            resource_data: Case data will be updated

        Returns:
            Updated case resource
        """
        return self._resource_action(resource_id, "POST", "complete", json=resource_data)

    def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to process state.

        Args:
            resource_id: Case resource ID
            resource_data: Case data will be updated

        Returns:
            Updated case resource
        """
        return self._resource_action(resource_id, "POST", "process", json=resource_data)

    def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to query state.

        Args:
            resource_id: Case resource ID
            resource_data: Case data will be updated

        Returns:
            Updated case resource
        """
        return self._resource_action(resource_id, "POST", "query", json=resource_data)


class AsyncCasesService(
    AsyncCollectionMixin[Case],
    AsyncCreateMixin[Case],
    AsyncGetMixin[Case],
    AsyncUpdateMixin[Case],
    AsyncService[Case],
    CasesServiceConfig,
):
    """Async cases service."""

    async def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to complete state.

        Args:
            resource_id: Case resource ID
            resource_data: Case data will be updated

        Returns:
            Updated case resource
        """
        return await self._resource_action(resource_id, "POST", "complete", json=resource_data)

    async def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to process state.

        Args:
            resource_id: Case resource ID
            resource_data: Case data will be updated

        Returns:
            Updated case resource
        """
        return await self._resource_action(resource_id, "POST", "process", json=resource_data)

    async def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Case:
        """Switch case to query state.

        Args:
            resource_id: Case resource ID
            resource_data: Case data will be updated

        Returns:
            Updated case resource
        """
        return await self._resource_action(resource_id, "POST", "query", json=resource_data)
