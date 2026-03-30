from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData


class Queue(Model):
    """Helpdesk Queue resource."""


class QueuesServiceConfig:
    """Helpdesk Queues service configuration."""

    _endpoint = "/public/v1/helpdesk/queues"
    _model_class = Queue
    _collection_key = "data"


class QueuesService(
    ManagedResourceMixin[Queue],
    CollectionMixin[Queue],
    Service[Queue],
    QueuesServiceConfig,
):
    """Helpdesk Queues service."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Queue:
        """Switch queue to active state."""
        return self._resource(resource_id).post("activate", json=resource_data)

    def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Queue:
        """Switch queue to disabled state."""
        return self._resource(resource_id).post("disable", json=resource_data)


class AsyncQueuesService(
    AsyncManagedResourceMixin[Queue],
    AsyncCollectionMixin[Queue],
    AsyncService[Queue],
    QueuesServiceConfig,
):
    """Async Helpdesk Queues service."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Queue:
        """Switch queue to active state."""
        return await self._resource(resource_id).post("activate", json=resource_data)

    async def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Queue:
        """Switch queue to disabled state."""
        return await self._resource(resource_id).post("disable", json=resource_data)
