from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData


class Contact(Model):
    """Notifications Contact resource."""


class ContactsServiceConfig:
    """Notifications Contacts service configuration."""

    _endpoint = "/public/v1/notifications/contacts"
    _model_class = Contact
    _collection_key = "data"


class ContactsService(
    ManagedResourceMixin[Contact],
    CollectionMixin[Contact],
    Service[Contact],
    ContactsServiceConfig,
):
    """Notifications Contacts service."""

    def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a contact."""
        return self._resource_action(resource_id, "POST", "block", json=resource_data)

    def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a contact."""
        return self._resource_action(resource_id, "POST", "unblock", json=resource_data)


class AsyncContactsService(
    AsyncManagedResourceMixin[Contact],
    AsyncCollectionMixin[Contact],
    AsyncService[Contact],
    ContactsServiceConfig,
):
    """Async Notifications Contacts service."""

    async def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a contact."""
        return await self._resource_action(resource_id, "POST", "block", json=resource_data)

    async def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a contact."""
        return await self._resource_action(resource_id, "POST", "unblock", json=resource_data)
