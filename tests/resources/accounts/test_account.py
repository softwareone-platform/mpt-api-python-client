import pytest

from mpt_api_client.resources.accounts.account import AccountsService, AsyncAccountsService
from mpt_api_client.resources.accounts.accounts_users import (
    AccountsUsersService,
    AsyncAccountsUsersService,
)


@pytest.fixture
def account_service(http_client):
    return AccountsService(http_client=http_client)


@pytest.fixture
def async_account_service(async_http_client):
    return AsyncAccountsService(http_client=async_http_client)


@pytest.fixture
def accounts_users_service(http_client):
    return AccountsUsersService(
        http_client=http_client, endpoint_params={"account_id": "ACC-0000-0001"}
    )


@pytest.fixture
def async_accounts_users_service(async_http_client):
    return AsyncAccountsUsersService(
        http_client=async_http_client, endpoint_params={"account_id": "ACC-0000-0001"}
    )


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "enable", "disable", "activate", "deactivate", "validate"]
)
def test_mixins_present(account_service, method):
    assert hasattr(account_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "enable", "disable", "activate", "deactivate", "validate"]
)
def test_async_mixins_present(async_account_service, method):
    assert hasattr(async_account_service, method)


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("users", AccountsUsersService),
    ],
)
def test_property_services(account_service, service_method, expected_service_class):
    service = getattr(account_service, service_method)("ACC-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"account_id": "ACC-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("users", AsyncAccountsUsersService),
    ],
)
def test_async_property_services(async_account_service, service_method, expected_service_class):
    service = getattr(async_account_service, service_method)("ACC-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"account_id": "ACC-0000-0001"}
