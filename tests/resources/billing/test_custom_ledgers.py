import pytest

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
