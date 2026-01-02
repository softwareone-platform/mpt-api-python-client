from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncAttachmentMixin, AttachmentMixin


class LedgerAttachment(Model):
    """Ledger Attachment resource."""


class LedgerAttachmentsServiceConfig:
    """Ledger Attachments service configuration."""

    _endpoint = "/public/v1/billing/ledgers/{ledger_id}/attachments"
    _model_class = LedgerAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class LedgerAttachmentsService(
    AttachmentMixin[LedgerAttachment],
    CollectionMixin[LedgerAttachment],
    Service[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""


class AsyncLedgerAttachmentsService(
    AsyncAttachmentMixin[LedgerAttachment],
    AsyncCollectionMixin[LedgerAttachment],
    AsyncService[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""
