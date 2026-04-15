from mpt_api_client.models import ResourceData


class PublishableMixin[Model]:
    """Publishable mixin adds the ability to publish and unpublish."""

    def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("publish", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("unpublish", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncPublishableMixin[Model]:
    """Publishable mixin adds the ability to publish and unpublish."""

    async def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("publish", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("unpublish", json=resource_data)  # type: ignore[attr-defined, no-any-return]
