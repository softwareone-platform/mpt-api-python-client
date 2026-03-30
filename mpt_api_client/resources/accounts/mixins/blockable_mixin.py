from mpt_api_client.models import ResourceData


class BlockableMixin[Model]:
    """Blockable mixin for blocking and unblocking resources."""

    def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("block", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("unblock", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncBlockableMixin[Model]:
    """Asynchronous Blockable mixin for blocking and unblocking resources."""

    async def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("block", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("unblock", json=resource_data)  # type: ignore[attr-defined, no-any-return]
