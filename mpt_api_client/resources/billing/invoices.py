from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncCreateMixin, AsyncUpdateMixin, CreateMixin, UpdateMixin
from mpt_api_client.models import Model


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
    Service[Invoice],
    InvoicesServiceConfig,
):
    """Invoices service."""


class AsyncInvoicesService(
    AsyncCreateMixin[Invoice],
    AsyncUpdateMixin[Invoice],
    AsyncService[Invoice],
    InvoicesServiceConfig,
):
    """Async Invoices service."""
