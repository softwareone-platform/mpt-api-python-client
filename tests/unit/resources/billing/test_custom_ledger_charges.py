import pytest

from mpt_api_client.resources.billing.custom_ledger_charges import (
    AsyncCustomLedgerChargesService,
    CustomLedgerChargesService,
)


@pytest.fixture
def custom_ledger_charges_service(http_client):
    return CustomLedgerChargesService(
        http_client=http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


@pytest.fixture
def async_custom_ledger_charges_service(async_http_client):
    return AsyncCustomLedgerChargesService(
        http_client=async_http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


def test_endpoint(custom_ledger_charges_service):
    assert custom_ledger_charges_service.path == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/charges"
    )


def test_async_endpoint(async_custom_ledger_charges_service):
    assert async_custom_ledger_charges_service.path == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/charges"
    )


@pytest.mark.parametrize("method", ["get"])
def test_methods_present(custom_ledger_charges_service, method):
    assert hasattr(custom_ledger_charges_service, method)


@pytest.mark.parametrize("method", ["get"])
def test_async_methods_present(async_custom_ledger_charges_service, method):
    assert hasattr(async_custom_ledger_charges_service, method)
