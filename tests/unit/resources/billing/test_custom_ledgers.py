import pytest

from mpt_api_client.resources.billing.custom_ledger_attachments import (
    AsyncCustomLedgerAttachmentsService,
    CustomLedgerAttachmentsService,
)
from mpt_api_client.resources.billing.custom_ledger_charges import (
    AsyncCustomLedgerChargesService,
    CustomLedgerChargesService,
)
from mpt_api_client.resources.billing.custom_ledger_upload import (
    AsyncCustomLedgerUploadService,
    CustomLedgerUploadService,
)
from mpt_api_client.resources.billing.custom_ledgers import (
    AsyncCustomLedgersService,
    CustomLedgersService,
)


@pytest.fixture
def custom_ledgers_service(http_client):
    return CustomLedgersService(http_client=http_client)


@pytest.fixture
def async_custom_ledgers_service(http_client):
    return AsyncCustomLedgersService(http_client=http_client)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "accept", "queue"])
def test_mixins_present(custom_ledgers_service, method):
    result = hasattr(custom_ledgers_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "accept", "queue"])
def test_async_mixins_present(async_custom_ledgers_service, method):
    result = hasattr(async_custom_ledgers_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", CustomLedgerChargesService),
        ("upload", CustomLedgerUploadService),
        ("attachments", CustomLedgerAttachmentsService),
    ],
)
def test_property_services(custom_ledgers_service, service_method, expected_service_class):
    result = getattr(custom_ledgers_service, service_method)("LDG-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"custom_ledger_id": "LDG-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", AsyncCustomLedgerChargesService),
        ("upload", AsyncCustomLedgerUploadService),
        ("attachments", AsyncCustomLedgerAttachmentsService),
    ],
)
def test_async_property_services(
    async_custom_ledgers_service, service_method, expected_service_class
):
    result = getattr(async_custom_ledgers_service, service_method)("LDG-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"custom_ledger_id": "LDG-0000-0001"}
