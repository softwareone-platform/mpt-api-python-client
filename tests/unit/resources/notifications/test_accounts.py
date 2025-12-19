import pytest

from mpt_api_client.resources.notifications.accounts import (
    AccountsService,
    AsyncAccountsService,
)


@pytest.fixture
def accounts_service(http_client):
    return AccountsService(http_client=http_client)


@pytest.fixture
def async_accounts_service(async_http_client):
    return AsyncAccountsService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["iterate"])
def test_sync_accounts_service_methods(accounts_service, method):
    result = hasattr(accounts_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["iterate"])
def test_async_accounts_service_methods(async_accounts_service, method):
    result = hasattr(async_accounts_service, method)

    assert result is True
