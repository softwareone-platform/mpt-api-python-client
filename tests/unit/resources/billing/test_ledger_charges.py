import pytest

from mpt_api_client.resources.billing.ledger_charges import (
    AsyncLedgerChargesService,
    LedgerChargesService,
)


@pytest.fixture
def ledger_charges_service(http_client):
    return LedgerChargesService(
        http_client=http_client, endpoint_params={"ledger_id": "LED-0000-0001"}
    )


@pytest.fixture
def async_ledger_charges_service(async_http_client):
    return AsyncLedgerChargesService(
        http_client=async_http_client, endpoint_params={"ledger_id": "LED-0000-0001"}
    )


def test_endpoint(ledger_charges_service):
    assert ledger_charges_service.path == "/public/v1/billing/ledgers/LED-0000-0001/charges"


def test_async_endpoint(async_ledger_charges_service):
    assert async_ledger_charges_service.path == "/public/v1/billing/ledgers/LED-0000-0001/charges"


@pytest.mark.parametrize("method", ["get"])
def test_methods_present(ledger_charges_service, method):
    assert hasattr(ledger_charges_service, method)


@pytest.mark.parametrize("method", ["get"])
def test_async_methods_present(async_ledger_charges_service, method):
    assert hasattr(async_ledger_charges_service, method)
