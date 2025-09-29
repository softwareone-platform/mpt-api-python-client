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


class LedgerAttachment(Model):
    """Ledger Attachment resource."""


class LedgerAttachmentsServiceConfig:
    """Ledger Attachments service configuration."""

    _endpoint = "/public/v1/billing/ledgers/{ledger_id}/attachments"
    _model_class = LedgerAttachment
    _collection_key = "data"


class LedgerAttachmentsService(
    FileOperationsMixin[LedgerAttachment],
    DeleteMixin,
    UpdateMixin[LedgerAttachment],
    Service[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""


class AsyncLedgerAttachmentsService(
    AsyncFileOperationsMixin[LedgerAttachment],
    AsyncDeleteMixin,
    AsyncUpdateMixin[LedgerAttachment],
    AsyncService[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""
