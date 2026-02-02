class GetMixin[Model]:
    """Get resource mixin."""

    def get(self, resource_id: str, select: list[str] | str | None = None) -> Model:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            select: List of fields to select.

        Returns:
            Resource object.
        """
        if isinstance(select, list):
            select = ",".join(select) if select else None

        return self._resource_action(resource_id=resource_id, query_params={"select": select})  # type: ignore[attr-defined, no-any-return]


class AsyncGetMixin[Model]:
    """Async get resource mixin."""

    async def get(self, resource_id: str, select: list[str] | str | None = None) -> Model:
        """Fetch a specific resource using `GET /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
            select: List of fields to select.

        Returns:
            Resource object.
        """
        if isinstance(select, list):
            select = ",".join(select) if select else None
        return await self._resource_action(resource_id=resource_id, query_params={"select": select})  # type: ignore[attr-defined, no-any-return]
