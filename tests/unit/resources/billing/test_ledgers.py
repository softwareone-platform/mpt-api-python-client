import pytest

from mpt_api_client.resources.billing.ledger_attachments import (
    AsyncLedgerAttachmentsService,
    LedgerAttachmentsService,
)
from mpt_api_client.resources.billing.ledger_charges import (
    AsyncLedgerChargesService,
    LedgerChargesService,
)
from mpt_api_client.resources.billing.ledgers import AsyncLedgersService, LedgersService


@pytest.fixture
def ledgers_service(http_client):
    return LedgersService(http_client=http_client)


@pytest.fixture
def async_ledgers_service(async_http_client):
    return AsyncLedgersService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create"],
)
def test_mixins_present(ledgers_service, method):
    assert hasattr(ledgers_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create"],
)
def test_async_mixins_present(async_ledgers_service, method):
    assert hasattr(async_ledgers_service, method)


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", LedgerChargesService),
        ("attachments", LedgerAttachmentsService),
    ],
)
def test_property_services(ledgers_service, service_method, expected_service_class):
    service = getattr(ledgers_service, service_method)("LED-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"ledger_id": "LED-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", AsyncLedgerChargesService),
        ("attachments", AsyncLedgerAttachmentsService),
    ],
)
def test_async_property_services(async_ledgers_service, service_method, expected_service_class):
    service = getattr(async_ledgers_service, service_method)("LED-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"ledger_id": "LED-0000-0001"}
