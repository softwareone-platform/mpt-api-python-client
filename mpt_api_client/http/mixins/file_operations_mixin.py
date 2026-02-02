from mpt_api_client.constants import APPLICATION_JSON
from mpt_api_client.http.client import json_to_file_payload
from mpt_api_client.http.mixins.download_file_mixin import (
    AsyncDownloadFileMixin,
    DownloadFileMixin,
)
from mpt_api_client.http.types import FileTypes
from mpt_api_client.models import ResourceData


class FilesOperationsMixin[Model](DownloadFileMixin[Model]):
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
                json_to_file_payload(resource_data),
                APPLICATION_JSON,
            )
        response = self.http_client.request("post", self.path, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncFilesOperationsMixin[Model](AsyncDownloadFileMixin[Model]):
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
                json_to_file_payload(resource_data),
                APPLICATION_JSON,
            )

        response = await self.http_client.request("post", self.path, files=files)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]
