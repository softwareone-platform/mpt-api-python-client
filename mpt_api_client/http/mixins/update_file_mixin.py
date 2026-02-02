from urllib.parse import urljoin

from mpt_api_client.http.types import FileTypes
from mpt_api_client.models import ResourceData


class UpdateFileMixin[Model]:
    """Update file mixin."""

    def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        file: FileTypes | None = None,  # noqa: WPS110
    ) -> Model:
        """Update file.

        Update a file resource by specifying a file.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Updated resource.
        """
        files = {}

        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncUpdateFileMixin[Model]:
    """Asynchronous Update file mixin."""

    async def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        file: FileTypes | None = None,  # noqa: WPS110
    ) -> Model:
        """Update file.

        Update a file resource by specifying a file.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Updated resource.
        """
        files = {}

        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = await self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]
