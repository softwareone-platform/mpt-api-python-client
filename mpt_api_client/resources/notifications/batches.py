from httpx._types import FileTypes

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
    _json_to_file_payload,
)
from mpt_api_client.models import FileModel, Model, ResourceData


class Batch(Model):
    """Notifications Batch resource."""


class BatchesServiceConfig:
    """Notifications Batches service configuration."""

    _endpoint = "/public/v1/notifications/batches"
    _model_class = Batch
    _collection_key = "data"


class BatchesService(
    GetMixin[Batch],
    CollectionMixin[Batch],
    Service[Batch],
    BatchesServiceConfig,
):
    """Notifications Batches service."""

    def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
        data_key: str = "_attachment_data",
    ) -> Model:
        """Create batch with attachments.

        Args:
            resource_data: batch data.
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

        response = self.http_client.request("post", self.path, files=files)
        return self._model_class.from_response(response)

    def get_batch_attachment(self, batch_id: str, attachment_id: str) -> FileModel:
        """Get batch attachment.

        Args:
            batch_id: Batch ID.
            attachment_id: Attachment ID.

        Returns:
            FileModel containing the attachment.
        """
        response = self.http_client.request(
            "get", f"{self.path}/{batch_id}/attachments/{attachment_id}"
        )

        return FileModel(response)


class AsyncBatchesService(
    AsyncGetMixin[Batch],
    AsyncCollectionMixin[Batch],
    AsyncService[Batch],
    BatchesServiceConfig,
):
    """Async Notifications Batches service."""

    async def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
        data_key: str = "_attachment_data",
    ) -> Model:
        """Create batch with attachments.

        Args:
            resource_data: batch data.
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

        response = await self.http_client.request("post", self.path, files=files)
        return self._model_class.from_response(response)

    async def get_batch_attachment(self, batch_id: str, attachment_id: str) -> FileModel:
        """Get batch attachment.

        Args:
            batch_id: Batch ID.
            attachment_id: Attachment ID.

        Returns:
            FileModel containing the attachment.
        """
        response = await self.http_client.request(
            "get", f"{self.path}/{batch_id}/attachments/{attachment_id}"
        )
        return FileModel(response)
