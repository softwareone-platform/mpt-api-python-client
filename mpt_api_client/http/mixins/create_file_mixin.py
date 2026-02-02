from mpt_api_client.http.types import FileTypes
from mpt_api_client.models import ResourceData


class CreateFileMixin[Model]:
    """Create file mixin."""

    def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:  # noqa: WPS110
        """Create logo.

        Create a file resource by specifying a file image.

        Args:
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncCreateFileMixin[Model]:
    """Asynchronous Create file mixin."""

    async def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:  # noqa: WPS110
        """Create file.

        Create a file resource by specifying a file.

        Args:
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file  # type: ignore[attr-defined]

        response = await self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,  # type: ignore[attr-defined]
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]
