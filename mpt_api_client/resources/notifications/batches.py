from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncGetMixin,
    CollectionMixin,
    CreateFileMixin,
    GetMixin,
)
from mpt_api_client.models import FileModel, Model


class Batch(Model):
    """Notifications Batch resource."""


class BatchAttachment(Model):
    """Notifications Batch Attachment resource."""


class BatchesServiceConfig:
    """Notifications Batches service configuration."""

    _endpoint = "/public/v1/notifications/batches"
    _model_class = Batch
    _collection_key = "data"
    _upload_file_key = "attachment"
    _upload_data_key = "batch"


class BatchesService(
    CreateFileMixin[Batch],
    GetMixin[Batch],
    CollectionMixin[Batch],
    Service[Batch],
    BatchesServiceConfig,
):
    """Notifications Batches service."""

    def get_attachment(self, batch_id: str, attachment_id: str) -> BatchAttachment:
        """Get batch attachment.

        Args:
            batch_id: Batch ID.
            attachment_id: Attachment ID.

        Returns:
            BatchAttachment containing the attachment data.
        """
        response = self.http_client.request(
            "get",
            f"{self.path}/{batch_id}/attachments/{attachment_id}",
            headers={"Accept": "application/json"},
        )

        return BatchAttachment.from_response(response)

    def download_attachment(self, batch_id: str, attachment_id: str) -> FileModel:
        """Download batch attachment.

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
    AsyncCreateFileMixin[Batch],
    AsyncGetMixin[Batch],
    AsyncCollectionMixin[Batch],
    AsyncService[Batch],
    BatchesServiceConfig,
):
    """Async Notifications Batches service."""

    async def get_attachment(self, batch_id: str, attachment_id: str) -> BatchAttachment:
        """Get batch attachment.

        Args:
            batch_id: Batch ID.
            attachment_id: Attachment ID.

        Returns:
            BatchAttachment containing the attachment data.
        """
        response = await self.http_client.request(
            "get",
            f"{self.path}/{batch_id}/attachments/{attachment_id}",
            headers={"Accept": "application/json"},
        )
        return BatchAttachment.from_response(response)

    async def download_attachment(self, batch_id: str, attachment_id: str) -> FileModel:
        """Download batch attachment.

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
