from mpt_api_client.models import ResourceData


class AcceptableMixin[Model]:
    """Acceptable mixin adds the ability to accept resources."""

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("accept", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("queue", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncAcceptableMixin[Model]:
    """Acceptable mixin adds the ability to accept resources."""

    async def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("accept", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("queue", json=resource_data)  # type: ignore[attr-defined, no-any-return]
