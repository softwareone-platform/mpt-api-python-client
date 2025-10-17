from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.invoice_attachments import (
    AsyncInvoiceAttachmentsService,
    InvoiceAttachmentsService,
)


class Invoice(Model):
    """Invoice resource."""


class InvoicesServiceConfig:
    """Invoices service configuration."""

    _endpoint = "/public/v1/billing/invoices"
    _model_class = Invoice
    _collection_key = "data"


class InvoicesService(
    CreateMixin[Invoice],
    UpdateMixin[Invoice],
    GetMixin[Invoice],
    CollectionMixin[Invoice],
    Service[Invoice],
    InvoicesServiceConfig,
):
    """Invoices service."""

    def attachments(self, invoice_id: str) -> InvoiceAttachmentsService:
        """Return invoice attachments service."""
        return InvoiceAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"invoice_id": invoice_id},
        )


class AsyncInvoicesService(
    AsyncCreateMixin[Invoice],
    AsyncUpdateMixin[Invoice],
    AsyncGetMixin[Invoice],
    AsyncCollectionMixin[Invoice],
    AsyncService[Invoice],
    InvoicesServiceConfig,
):
    """Async Invoices service."""

    def attachments(self, invoice_id: str) -> AsyncInvoiceAttachmentsService:
        """Return invoice attachments service."""
        return AsyncInvoiceAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"invoice_id": invoice_id},
        )
