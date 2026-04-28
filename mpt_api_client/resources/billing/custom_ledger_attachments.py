from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import AttachmentModel
from mpt_api_client.resources.billing.mixins import AsyncAttachmentMixin, AttachmentMixin


class CustomLedgerAttachment(AttachmentModel):
    """Custom Ledger Attachment resource. Inherits fields from AttachmentModel."""


class CustomLedgerAttachmentsServiceConfig:
    """Custom Ledger Attachments service configuration."""

    _endpoint = "/public/v1/billing/custom-ledgers/{custom_ledger_id}/attachments"
    _model_class = CustomLedgerAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class CustomLedgerAttachmentsService(
    AttachmentMixin[CustomLedgerAttachment],
    CollectionMixin[CustomLedgerAttachment],
    Service[CustomLedgerAttachment],
    CustomLedgerAttachmentsServiceConfig,
):
    """Custom Ledger Attachments service."""


class AsyncCustomLedgerAttachmentsService(
    AsyncAttachmentMixin[CustomLedgerAttachment],
    AsyncCollectionMixin[CustomLedgerAttachment],
    AsyncService[CustomLedgerAttachment],
    CustomLedgerAttachmentsServiceConfig,
):
    """Custom Ledger Attachments service."""
