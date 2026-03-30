class DeleteMixin:
    """Delete resource mixin."""

    def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        self._resource(resource_id).delete()  # type: ignore[attr-defined]


class AsyncDeleteMixin:
    """Delete resource mixin."""

    async def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        await self._resource(resource_id).delete()  # type: ignore[attr-defined]
