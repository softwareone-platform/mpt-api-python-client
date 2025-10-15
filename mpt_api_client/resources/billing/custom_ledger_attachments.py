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


class CustomLedgerAttachment(Model):
    """Custom Ledger Attachment resource."""


class CustomLedgerAttachmentsServiceConfig:
    """Custom Ledger Attachments service configuration."""

    _endpoint = "/public/v1/billing/custom-ledgers/{custom_ledger_id}/attachments"
    _model_class = CustomLedgerAttachment
    _collection_key = "data"


class CustomLedgerAttachmentsService(
    FileOperationsMixin[CustomLedgerAttachment],
    DeleteMixin,
    GetMixin[CustomLedgerAttachment],
    UpdateMixin[CustomLedgerAttachment],
    Service[CustomLedgerAttachment],
    CustomLedgerAttachmentsServiceConfig,
):
    """Custom Ledger Attachments service."""


class AsyncCustomLedgerAttachmentsService(
    AsyncFileOperationsMixin[CustomLedgerAttachment],
    AsyncDeleteMixin,
    AsyncGetMixin[CustomLedgerAttachment],
    AsyncUpdateMixin[CustomLedgerAttachment],
    AsyncService[CustomLedgerAttachment],
    CustomLedgerAttachmentsServiceConfig,
):
    """Custom Ledger Attachments service."""
