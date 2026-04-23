from mpt_api_client.models import ResourceData


class PublishableMixin[Model]:
    """Publishable mixin adds the ability to publish and unpublish a resource."""

    def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Publish the resource."""
        return self._resource(resource_id).post("publish", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unpublish the resource."""
        return self._resource(resource_id).post("unpublish", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncPublishableMixin[Model]:
    """Async publishable mixin adds the ability to publish and unpublish a resource."""

    async def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Publish the resource."""
        return await self._resource(resource_id).post("publish", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unpublish the resource."""
        return await self._resource(resource_id).post("unpublish", json=resource_data)  # type: ignore[attr-defined, no-any-return]
