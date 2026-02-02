from mpt_api_client.models import ResourceData


class UpdateMixin[Model]:
    """Update resource mixin."""

    def update(self, resource_id: str, resource_data: ResourceData) -> Model:
        """Update a resource using `PUT /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.

        Returns:
            Resource object.

        """
        return self._resource_action(resource_id, "PUT", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncUpdateMixin[Model]:
    """Update resource mixin."""

    async def update(self, resource_id: str, resource_data: ResourceData) -> Model:
        """Update a resource using `PUT /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.

        Returns:
            Resource object.

        """
        return await self._resource_action(resource_id, "PUT", json=resource_data)  # type: ignore[attr-defined, no-any-return]
