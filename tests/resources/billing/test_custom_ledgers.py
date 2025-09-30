import pytest

from mpt_api_client.resources.billing.custom_ledger_charges import (
    AsyncCustomLedgerChargesService,
    CustomLedgerChargesService,
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
    assert hasattr(custom_ledgers_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "accept", "queue"])
def test_async_mixins_present(async_custom_ledgers_service, method):
    assert hasattr(async_custom_ledgers_service, method)


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", CustomLedgerChargesService),
    ],
)
def test_property_services(custom_ledgers_service, service_method, expected_service_class):
    service = getattr(custom_ledgers_service, service_method)("LDG-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"custom_ledger_id": "LDG-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", AsyncCustomLedgerChargesService),
    ],
)
def test_async_property_services(
    async_custom_ledgers_service, service_method, expected_service_class
):
    service = getattr(async_custom_ledgers_service, service_method)("LDG-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"custom_ledger_id": "LDG-0000-0001"}
