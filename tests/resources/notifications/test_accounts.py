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
