import pytest

from mpt_api_client.resources.billing.custom_ledger_upload import (
    AsyncCustomLedgerUploadService,
    CustomLedgerUploadService,
)


@pytest.fixture
def custom_ledger_upload_service(http_client):
    return CustomLedgerUploadService(
        http_client=http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


@pytest.fixture
def async_custom_ledger_upload_service(http_client):
    return AsyncCustomLedgerUploadService(
        http_client=http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


def test_endpoint(custom_ledger_upload_service):
    assert custom_ledger_upload_service.endpoint == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/upload"
    )


def test_async_endpoint(async_custom_ledger_upload_service):
    assert async_custom_ledger_upload_service.endpoint == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/upload"
    )


@pytest.mark.parametrize("method", ["create"])
def test_mixins_present(custom_ledger_upload_service, method):
    assert hasattr(custom_ledger_upload_service, method)


@pytest.mark.parametrize("method", ["create"])
def test_async_mixins_present(async_custom_ledger_upload_service, method):
    assert hasattr(async_custom_ledger_upload_service, method)
