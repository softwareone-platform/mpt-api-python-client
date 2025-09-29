import pytest

from mpt_api_client.resources.billing.ledger_attachments import (
    AsyncLedgerAttachmentsService,
    LedgerAttachmentsService,
)


@pytest.fixture
def ledger_attachments_service(http_client) -> LedgerAttachmentsService:
    return LedgerAttachmentsService(
        http_client=http_client, endpoint_params={"ledger_id": "LED-0000-0001"}
    )


@pytest.fixture
def async_ledger_attachments_service(async_http_client) -> AsyncLedgerAttachmentsService:
    return AsyncLedgerAttachmentsService(
        http_client=async_http_client, endpoint_params={"ledger_id": "LED-0000-0001"}
    )


def test_endpoint(ledger_attachments_service) -> None:
    assert (
        ledger_attachments_service.endpoint
        == "/public/v1/billing/ledgers/LED-0000-0001/attachments"
    )


def test_async_endpoint(async_ledger_attachments_service) -> None:
    assert (
        async_ledger_attachments_service.endpoint
        == "/public/v1/billing/ledgers/LED-0000-0001/attachments"
    )


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_methods_present(ledger_attachments_service, method: str) -> None:
    assert hasattr(ledger_attachments_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_methods_present(async_ledger_attachments_service, method: str) -> None:
    assert hasattr(async_ledger_attachments_service, method)
