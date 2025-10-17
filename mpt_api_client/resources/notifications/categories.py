from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData


class Category(Model):
    """Notifications Category resource."""


class CategoriesServiceConfig:
    """Notifications Categories service configuration."""

    _endpoint = "/public/v1/notifications/categories"
    _model_class = Category
    _collection_key = "data"


class CategoriesService(
    ManagedResourceMixin[Category],
    CollectionMixin[Category],
    Service[Category],
    CategoriesServiceConfig,
):
    """Notifications Categories service."""

    def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(resource_id, "POST", "publish", json=resource_data)

    def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(resource_id, "POST", "unpublish", json=resource_data)


class AsyncCategoriesService(
    AsyncManagedResourceMixin[Category],
    AsyncCollectionMixin[Category],
    AsyncService[Category],
    CategoriesServiceConfig,
):
    """Async Notifications Categories service."""

    async def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(resource_id, "POST", "publish", json=resource_data)

    async def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(resource_id, "POST", "unpublish", json=resource_data)
