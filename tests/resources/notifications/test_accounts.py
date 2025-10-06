import pytest

from mpt_api_client.resources.notifications.accounts import (
    AccountsService,
    AsyncAccountsService,
    MethodNotAllowedError,
)


@pytest.fixture
def accounts_service(http_client):
    return AccountsService(http_client=http_client)


@pytest.fixture
def async_accounts_service(async_http_client):
    return AsyncAccountsService(http_client=async_http_client)


def test_accounts_service_get_raises(accounts_service):
    with pytest.raises(MethodNotAllowedError):
        accounts_service.get("CONTACT-123")


@pytest.mark.asyncio
async def test_async_accounts_service_get_raises(async_accounts_service):
    with pytest.raises(MethodNotAllowedError):
        await async_accounts_service.get("CONTACT-123")
