import pytest

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
def test_mixins_present(invoices_service, method):
    assert hasattr(invoices_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_async_mixins_present(async_invoices_service, method):
    assert hasattr(async_invoices_service, method)
