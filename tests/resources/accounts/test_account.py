import pytest

from mpt_api_client.resources.accounts.account import AccountsService, AsyncAccountsService


@pytest.fixture
def account_service(http_client):
    return AccountsService(http_client=http_client)


@pytest.fixture
def async_account_service(async_http_client):
    return AsyncAccountsService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create", "update"])
def test_mixins_present(account_service, method):
    assert hasattr(account_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update"])
def test_async_mixins_present(async_account_service, method):
    assert hasattr(async_account_service, method)
