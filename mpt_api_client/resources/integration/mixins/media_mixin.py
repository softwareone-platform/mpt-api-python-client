from mpt_api_client.http.types import FileTypes
from mpt_api_client.http.url_utils import join_url_path


class MediaMixin[Model]:
    """Mixin that adds media-specific actions: upload_image."""

    def upload_image(self, resource_id: str, file: FileTypes) -> Model:  # noqa: WPS110
        """Upload or replace the image binary for this media item.

        Args:
            resource_id: Media item ID.
            file: Binary image file to upload.

        Returns:
            Updated media item.
        """
        url = join_url_path(self.path, resource_id, "image")  # type: ignore[attr-defined]
        response = self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            files={"file": file},
        )
        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncMediaMixin[Model]:
    """Async mixin that adds media-specific actions: upload_image."""

    async def upload_image(self, resource_id: str, file: FileTypes) -> Model:  # noqa: WPS110
        """Upload or replace the image binary for this media item.

        Args:
            resource_id: Media item ID.
            file: Binary image file to upload.

        Returns:
            Updated media item.
        """
        url = join_url_path(self.path, resource_id, "image")  # type: ignore[attr-defined]
        response = await self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            files={"file": file},
        )
        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]
