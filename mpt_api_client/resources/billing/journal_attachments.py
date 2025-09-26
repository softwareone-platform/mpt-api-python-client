from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncDeleteMixin,
    AsyncFileOperationsMixin,
    AsyncUpdateMixin,
    DeleteMixin,
    FileOperationsMixin,
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


class JournalAttachmentsService(
    FileOperationsMixin[JournalAttachment],
    DeleteMixin,
    UpdateMixin[JournalAttachment],
    Service[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""


class AsyncJournalAttachmentsService(
    AsyncFileOperationsMixin[JournalAttachment],
    AsyncDeleteMixin,
    AsyncUpdateMixin[JournalAttachment],
    AsyncService[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""
