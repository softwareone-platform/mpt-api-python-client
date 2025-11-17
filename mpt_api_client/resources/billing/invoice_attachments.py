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


class InvoiceAttachment(Model):
    """Invoice Attachment resource."""


class InvoiceAttachmentsServiceConfig:
    """Invoice Attachments service configuration."""

    _endpoint = "/public/v1/billing/invoices/{invoice_id}/attachments"
    _model_class = InvoiceAttachment
    _collection_key = "data"


class InvoiceAttachmentsService(
    FilesOperationsMixin[InvoiceAttachment],
    ModifiableResourceMixin[InvoiceAttachment],
    CollectionMixin[InvoiceAttachment],
    Service[InvoiceAttachment],
    InvoiceAttachmentsServiceConfig,
):
    """Invoice Attachments service."""


class AsyncInvoiceAttachmentsService(
    AsyncFilesOperationsMixin[InvoiceAttachment],
    AsyncModifiableResourceMixin[InvoiceAttachment],
    AsyncCollectionMixin[InvoiceAttachment],
    AsyncService[InvoiceAttachment],
    InvoiceAttachmentsServiceConfig,
):
    """Invoice Attachments service."""
