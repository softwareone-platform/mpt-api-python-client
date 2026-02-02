from mpt_api_client.models import ResourceData


class RecalculatableMixin[Model]:
    """Recalculatable mixin adds the ability to recalculate resources."""

    def recalculate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )

    def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )


class AsyncRecalculatableMixin[Model]:
    """Recalculatable mixin adds the ability to recalculate resources."""

    async def recalculate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )

    async def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )

    async def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )
