from urllib.parse import urljoin

from mpt_api_client.models import ResourceData


class CreateMixin[Model]:
    """Create resource mixin."""

    def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = self.http_client.post(self._endpoint, json=resource_data)  # type: ignore[attr-defined]
        response.raise_for_status()

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class DeleteMixin:
    """Delete resource mixin."""

    def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        response = self._resource_do_request(resource_id, "DELETE")  # type: ignore[attr-defined]
        response.raise_for_status()


class AsyncCreateMixin[Model]:
    """Create resource mixin."""

    async def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = await self.http_client.post(self._endpoint, json=resource_data)  # type: ignore[attr-defined]
        response.raise_for_status()

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncDeleteMixin:
    """Delete resource mixin."""

    async def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        url = urljoin(f"{self._endpoint}/", resource_id)  # type: ignore[attr-defined]
        response = await self.http_client.delete(url)  # type: ignore[attr-defined]
        response.raise_for_status()
