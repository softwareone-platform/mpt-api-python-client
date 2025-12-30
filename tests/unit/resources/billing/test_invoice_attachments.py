import pytest

from mpt_api_client.resources.billing.invoice_attachments import (
    AsyncInvoiceAttachmentsService,
    InvoiceAttachmentsService,
)


@pytest.fixture
def invoice_attachments_service(http_client):
    return InvoiceAttachmentsService(
        http_client=http_client, endpoint_params={"invoice_id": "INV-0000-0001"}
    )


@pytest.fixture
def async_invoice_attachments_service(async_http_client):
    return AsyncInvoiceAttachmentsService(
        http_client=async_http_client, endpoint_params={"invoice_id": "INV-0000-0001"}
    )


def test_endpoint(invoice_attachments_service):
    result = (
        invoice_attachments_service.path == "/public/v1/billing/invoices/INV-0000-0001/attachments"
    )

    assert result is True


def test_async_endpoint(async_invoice_attachments_service):
    result = (
        async_invoice_attachments_service.path
        == "/public/v1/billing/invoices/INV-0000-0001/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_methods_present(invoice_attachments_service, method: str):
    result = hasattr(invoice_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_async_methods_present(async_invoice_attachments_service, method: str):
    result = hasattr(async_invoice_attachments_service, method)

    assert result is True
