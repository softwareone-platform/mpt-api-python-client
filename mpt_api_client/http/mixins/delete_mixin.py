from urllib.parse import urljoin


class DeleteMixin:
    """Delete resource mixin."""

    def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        self._resource_do_request(resource_id, "DELETE")  # type: ignore[attr-defined]


class AsyncDeleteMixin:
    """Delete resource mixin."""

    async def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]
        await self.http_client.request("delete", url)  # type: ignore[attr-defined]
