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


class InvoiceAttachment(Model):
    """Invoice Attachment resource."""


class InvoiceAttachmentsServiceConfig:
    """Invoice Attachments service configuration."""

    _endpoint = "/public/v1/billing/invoices/{invoice_id}/attachments"
    _model_class = InvoiceAttachment
    _collection_key = "data"


class InvoiceAttachmentsService(
    FileOperationsMixin[InvoiceAttachment],
    DeleteMixin,
    UpdateMixin[InvoiceAttachment],
    Service[InvoiceAttachment],
    InvoiceAttachmentsServiceConfig,
):
    """Invoice Attachments service."""


class AsyncInvoiceAttachmentsService(
    AsyncFileOperationsMixin[InvoiceAttachment],
    AsyncDeleteMixin,
    AsyncUpdateMixin[InvoiceAttachment],
    AsyncService[InvoiceAttachment],
    InvoiceAttachmentsServiceConfig,
):
    """Invoice Attachments service."""
