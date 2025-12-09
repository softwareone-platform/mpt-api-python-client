from mpt_api_client.models.model import ResourceData


class TerminateMixin[Model]:
    """Terminate resource mixin."""

    def terminate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Terminate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data

        Returns:
            Terminated resource.
        """
        return self._resource_action(resource_id, "POST", "terminate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncTerminateMixin[Model]:
    """Asynchronous terminate resource mixin."""

    async def terminate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Terminate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data

        Returns:
            Terminated resource.
        """
        return await self._resource_action(resource_id, "POST", "terminate", json=resource_data)  # type: ignore[attr-defined, no-any-return]
