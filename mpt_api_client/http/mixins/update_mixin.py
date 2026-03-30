from mpt_api_client.models import ResourceData


class UpdateMixin[Model]:
    """Update resource mixin."""

    def update(self, resource_id: str, resource_data: ResourceData) -> Model:
        """Update a resource using `PUT /endpoint/{resource_id}`."""
        return self._resource(resource_id).put(json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncUpdateMixin[Model]:
    """Update resource mixin."""

    async def update(self, resource_id: str, resource_data: ResourceData) -> Model:
        """Update a resource using `PUT /endpoint/{resource_id}`."""
        return await self._resource(resource_id).put(json=resource_data)  # type: ignore[attr-defined, no-any-return]
