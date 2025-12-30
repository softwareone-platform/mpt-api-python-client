from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncAttachmentMixin, AttachmentMixin


class InvoiceAttachment(Model):
    """Invoice Attachment resource."""


class InvoiceAttachmentsServiceConfig:
    """Invoice Attachments service configuration."""

    _endpoint = "/public/v1/billing/invoices/{invoice_id}/attachments"
    _model_class = InvoiceAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class InvoiceAttachmentsService(
    AttachmentMixin[InvoiceAttachment],
    CollectionMixin[InvoiceAttachment],
    Service[InvoiceAttachment],
    InvoiceAttachmentsServiceConfig,
):
    """Invoice Attachments service."""


class AsyncInvoiceAttachmentsService(
    AsyncAttachmentMixin[InvoiceAttachment],
    AsyncCollectionMixin[InvoiceAttachment],
    AsyncService[InvoiceAttachment],
    InvoiceAttachmentsServiceConfig,
):
    """Invoice Attachments service."""
