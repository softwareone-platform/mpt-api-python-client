import pytest

from mpt_api_client.resources.billing.invoice_attachments import (
    AsyncInvoiceAttachmentsService,
    InvoiceAttachmentsService,
)
from mpt_api_client.resources.billing.invoices import (
    AsyncInvoicesService,
    InvoicesService,
)


@pytest.fixture
def invoices_service(http_client):
    return InvoicesService(http_client=http_client)


@pytest.fixture
def async_invoices_service(async_http_client):
    return AsyncInvoicesService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_methods_present(invoices_service, method):
    assert hasattr(invoices_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_async_methods_present(async_invoices_service, method):
    assert hasattr(async_invoices_service, method)


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", InvoiceAttachmentsService),
    ],
)
def test_property_services(invoices_service, service_method, expected_service_class):
    service = getattr(invoices_service, service_method)("INV-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"invoice_id": "INV-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", AsyncInvoiceAttachmentsService),
    ],
)
def test_async_property_services(async_invoices_service, service_method, expected_service_class):
    service = getattr(async_invoices_service, service_method)("INV-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"invoice_id": "INV-0000-0001"}
