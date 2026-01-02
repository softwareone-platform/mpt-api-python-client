from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncAttachmentMixin, AttachmentMixin


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
    AttachmentMixin[JournalAttachment],
    CollectionMixin[JournalAttachment],
    Service[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""


class AsyncJournalAttachmentsService(
    AsyncAttachmentMixin[JournalAttachment],
    AsyncCollectionMixin[JournalAttachment],
    AsyncService[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""
