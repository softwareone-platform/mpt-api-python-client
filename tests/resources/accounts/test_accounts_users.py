import pytest

from mpt_api_client.resources.accounts.accounts_user_groups import (
    AccountsUserGroupsService,
    AsyncAccountsUserGroupsService,
)
from mpt_api_client.resources.accounts.accounts_users import (
    AccountsUsersService,
    AsyncAccountsUsersService,
)


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


def test_endpoint(accounts_users_service):
    assert accounts_users_service.path == "/public/v1/accounts/ACC-0000-0001/users"


def test_async_endpoint(async_accounts_users_service):
    assert async_accounts_users_service.path == "/public/v1/accounts/ACC-0000-0001/users"


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "accept_invite", "resend_invite", "send_new_invite"],
)
def test_methods_present(accounts_users_service, method):
    assert hasattr(accounts_users_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "accept_invite", "resend_invite", "send_new_invite"],
)
def test_async_methods_present(async_accounts_users_service, method):
    assert hasattr(async_accounts_users_service, method)


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [("groups", AccountsUserGroupsService)],
)
def test_property_services(accounts_users_service, service_method, expected_service_class):
    service = getattr(accounts_users_service, service_method)("USR-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {
        "account_id": "ACC-0000-0001",
        "user_id": "USR-0000-0001",
    }


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [("groups", AsyncAccountsUserGroupsService)],
)
def test_async_property_services(
    async_accounts_users_service, service_method, expected_service_class
):
    service = getattr(async_accounts_users_service, service_method)("USR-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {
        "account_id": "ACC-0000-0001",
        "user_id": "USR-0000-0001",
    }
