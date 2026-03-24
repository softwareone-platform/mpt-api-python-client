from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData


class Form(Model):
    """Helpdesk Form resource."""


class FormsServiceConfig:
    """Helpdesk Forms service configuration."""

    _endpoint = "/public/v1/helpdesk/forms"
    _model_class = Form
    _collection_key = "data"


class FormsService(
    ManagedResourceMixin[Form],
    CollectionMixin[Form],
    Service[Form],
    FormsServiceConfig,
):
    """Helpdesk Forms service."""

    def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Form:
        """Switch form to published state."""
        return self._resource_action(resource_id, "POST", "publish", json=resource_data)

    def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Form:
        """Switch form to unpublished state."""
        return self._resource_action(resource_id, "POST", "unpublish", json=resource_data)


class AsyncFormsService(
    AsyncManagedResourceMixin[Form],
    AsyncCollectionMixin[Form],
    AsyncService[Form],
    FormsServiceConfig,
):
    """Async Helpdesk Forms service."""

    async def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Form:
        """Switch form to published state."""
        return await self._resource_action(resource_id, "POST", "publish", json=resource_data)

    async def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Form:
        """Switch form to unpublished state."""
        return await self._resource_action(resource_id, "POST", "unpublish", json=resource_data)
