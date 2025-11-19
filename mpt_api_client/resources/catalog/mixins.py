from mpt_api_client.http.mixins import (
    AsyncDownloadFileMixin,
    DownloadFileMixin,
)
from mpt_api_client.http.types import FileTypes
from mpt_api_client.models import ResourceData


# TODO: Consider moving publishable and activatable mixins to http/mixins
class PublishableMixin[Model]:
    """Publishable mixin adds the ability to review, publish and unpublish."""

    def review(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Pending.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "review", json=resource_data
        )

    def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "publish", json=resource_data
        )

    def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unpublish", json=resource_data
        )


class AsyncPublishableMixin[Model]:
    """Publishable mixin adds the ability to review, publish and unpublish."""

    async def review(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to reviewing.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "review", json=resource_data
        )

    async def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "publish", json=resource_data
        )

    async def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unpublish", json=resource_data
        )


class AsyncCreateFileMixin[Model]:
    """Create file mixin."""

    _upload_file_key = "file"
    _upload_data_key = "document"

    async def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:
        """Create document.

        Creates a document resource by specifying a `file` or an `url`.

        Args:
            resource_data: Resource data.
            file: File to upload.

        Returns:
            Created resource.
        """
        files = {}
        if file:
            files[self._upload_file_key] = file
        response = await self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,
            force_multipart=True,
        )
        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncDocumentMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncDownloadFileMixin[Model],
    AsyncPublishableMixin[Model],
):
    """Async document mixin."""


class CreateFileMixin[Model]:
    """Create file mixin."""

    _upload_file_key = "file"
    _upload_data_key = "document"

    def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:
        """Create document.

        Creates a document resource by specifying a `file` or an `url`.

        Args:
            resource_data: Resource data.
            file: File to upload.

        Returns:
            Created resource.
        """
        files = {}
        if file:
            files[self._upload_file_key] = file
        response = self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,
            force_multipart=True,
        )
        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class DocumentMixin[Model](
    CreateFileMixin[Model],
    DownloadFileMixin[Model],
    PublishableMixin[Model],
):
    """Document mixin."""

    _upload_file_key = "file"
    _upload_data_key = "document"


class MediaMixin[Model](
    CreateFileMixin[Model],
    DownloadFileMixin[Model],
    PublishableMixin[Model],
):
    """Document mixin."""

    _upload_file_key = "file"
    _upload_data_key = "media"


class ActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    def deactivate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Inactive.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class AsyncActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    async def deactivate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Update state to Inactive.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )
