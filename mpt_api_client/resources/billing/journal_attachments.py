from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncDownloadFileMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateFileMixin,
    DeleteMixin,
    DownloadFileMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model


class JournalAttachment(Model):
    """Journal Attachment resource."""


class JournalAttachmentsServiceConfig:
    """Journal Attachments service configuration."""

    _endpoint = "/public/v1/billing/journals/{journal_id}/attachments"
    _model_class = JournalAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class JournalAttachmentsService(
    CreateFileMixin[JournalAttachment],
    UpdateMixin[JournalAttachment],
    DownloadFileMixin[JournalAttachment],
    DeleteMixin,
    GetMixin[JournalAttachment],
    CollectionMixin[JournalAttachment],
    Service[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""


class AsyncJournalAttachmentsService(
    AsyncCreateFileMixin[JournalAttachment],
    AsyncUpdateMixin[JournalAttachment],
    AsyncDownloadFileMixin[JournalAttachment],
    AsyncDeleteMixin,
    AsyncGetMixin[JournalAttachment],
    AsyncCollectionMixin[JournalAttachment],
    AsyncService[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""
