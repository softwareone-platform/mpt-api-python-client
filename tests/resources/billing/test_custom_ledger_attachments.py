import pytest

from mpt_api_client.resources.billing.custom_ledger_attachments import (
    AsyncCustomLedgerAttachmentsService,
    CustomLedgerAttachmentsService,
)


@pytest.fixture
def custom_ledger_attachments_service(http_client):
    return CustomLedgerAttachmentsService(
        http_client=http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


@pytest.fixture
def async_custom_ledger_attachments_service(async_http_client):
    return AsyncCustomLedgerAttachmentsService(
        http_client=async_http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


def test_endpoint(custom_ledger_attachments_service):
    assert custom_ledger_attachments_service.path == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/attachments"
    )


def test_async_endpoint(async_custom_ledger_attachments_service):
    assert async_custom_ledger_attachments_service.path == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/attachments"
    )


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_methods_present(custom_ledger_attachments_service, method: str):
    assert hasattr(custom_ledger_attachments_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_methods_present(async_custom_ledger_attachments_service, method: str):
    assert hasattr(async_custom_ledger_attachments_service, method)
