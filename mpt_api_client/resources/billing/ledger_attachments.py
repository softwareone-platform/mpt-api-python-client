from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncFilesOperationsMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    FilesOperationsMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model


class LedgerAttachment(Model):
    """Ledger Attachment resource."""


class LedgerAttachmentsServiceConfig:
    """Ledger Attachments service configuration."""

    _endpoint = "/public/v1/billing/ledgers/{ledger_id}/attachments"
    _model_class = LedgerAttachment
    _collection_key = "data"


class LedgerAttachmentsService(
    FilesOperationsMixin[LedgerAttachment],
    ModifiableResourceMixin[LedgerAttachment],
    CollectionMixin[LedgerAttachment],
    Service[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""


class AsyncLedgerAttachmentsService(
    AsyncFilesOperationsMixin[LedgerAttachment],
    AsyncModifiableResourceMixin[LedgerAttachment],
    AsyncCollectionMixin[LedgerAttachment],
    AsyncService[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""
