import pytest

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
