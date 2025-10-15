from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncDeleteMixin,
    AsyncFileOperationsMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    DeleteMixin,
    FileOperationsMixin,
    GetMixin,
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
    GetMixin[LedgerAttachment],
    UpdateMixin[LedgerAttachment],
    Service[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""


class AsyncLedgerAttachmentsService(
    AsyncFileOperationsMixin[LedgerAttachment],
    AsyncDeleteMixin,
    AsyncGetMixin[LedgerAttachment],
    AsyncUpdateMixin[LedgerAttachment],
    AsyncService[LedgerAttachment],
    LedgerAttachmentsServiceConfig,
):
    """Ledger Attachments service."""
