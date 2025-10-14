import json
from urllib.parse import urljoin

from mpt_api_client.http.types import FileTypes, Response
from mpt_api_client.models import FileModel, ResourceData


def _json_to_file_payload(resource_data: ResourceData) -> bytes:
    return json.dumps(
        resource_data, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


class CreateMixin[Model]:
    """Create resource mixin."""

    def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = self.http_client.request("post", self.endpoint, json=resource_data)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class DeleteMixin:
    """Delete resource mixin."""

    def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        self._resource_do_request(resource_id, "DELETE")  # type: ignore[attr-defined]


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


class FileOperationsMixin[Model]:
    """Mixin that provides create and download methods for file-based resources."""

    def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
        data_key: str = "_attachment_data",
    ) -> Model:
        """Create resource with file support.

        Args:
            resource_data: Resource data.
            files: Files data.
            data_key: Key to use for the JSON data in the multipart form.

        Returns:
            Created resource.
        """
        files = files or {}

        if resource_data:
            files[data_key] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = self.http_client.request("post", self.endpoint, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]

    def download(self, resource_id: str) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.

        Returns:
            File model containing the downloaded file.
        """
        response: Response = self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)


class AsyncCreateMixin[Model]:
    """Create resource mixin."""

    async def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = await self.http_client.request("post", self.endpoint, json=resource_data)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncDeleteMixin:
    """Delete resource mixin."""

    async def delete(self, resource_id: str) -> None:
        """Delete resource using `DELETE /endpoint/{resource_id}`.

        Args:
            resource_id: Resource ID.
        """
        url = urljoin(f"{self.endpoint}/", resource_id)  # type: ignore[attr-defined]
        await self.http_client.request("delete", url)  # type: ignore[attr-defined]


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


class AsyncFileOperationsMixin[Model]:
    """Async mixin that provides create and download methods for file-based resources."""

    async def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
        data_key: str = "_attachment_data",
    ) -> Model:
        """Create resource with file support.

        Args:
            resource_data: Resource data.
            files: Files data.
            data_key: Key to use for the JSON data in the multipart form.

        Returns:
            Created resource.
        """
        files = files or {}

        if resource_data:
            files[data_key] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = await self.http_client.request("post", self.endpoint, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]

    async def download(self, resource_id: str) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.

        Returns:
            File model containing the downloaded file.
        """
        response = await self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)


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
