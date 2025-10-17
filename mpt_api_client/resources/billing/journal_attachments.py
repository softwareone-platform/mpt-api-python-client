from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncFileOperationsMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    FileOperationsMixin,
    ModifiableResourceMixin,
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
    ModifiableResourceMixin[JournalAttachment],
    CollectionMixin[JournalAttachment],
    Service[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""


class AsyncJournalAttachmentsService(
    AsyncFileOperationsMixin[JournalAttachment],
    AsyncModifiableResourceMixin[JournalAttachment],
    AsyncCollectionMixin[JournalAttachment],
    AsyncService[JournalAttachment],
    JournalAttachmentsServiceConfig,
):
    """Journal Attachments service."""
