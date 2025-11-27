import pytest

from mpt_api_client.resources.accounts.account_user_groups import (
    AccountUserGroupsService,
    AsyncAccountUserGroupsService,
)
from mpt_api_client.resources.accounts.account_users import (
    AccountUsersService,
    AsyncAccountUsersService,
)


@pytest.fixture
def account_users_service(http_client):
    return AccountUsersService(http_client=http_client)


@pytest.fixture
def async_account_users_service(http_client):
    return AsyncAccountUsersService(http_client=http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "accept_invite", "resend_invite", "send_new_invite"],
)
def test_methods_present(account_users_service, method):
    result = hasattr(account_users_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "accept_invite", "resend_invite", "send_new_invite"],
)
def test_async_methods_present(async_account_users_service, method):
    result = hasattr(async_account_users_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("groups", AccountUserGroupsService),
    ],
)
def test_property_services(account_users_service, service_method, expected_service_class):
    result = getattr(account_users_service, service_method)("ACC-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"account_user_id": "ACC-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("groups", AsyncAccountUserGroupsService),
    ],
)
def test_async_property_services(
    async_account_users_service, service_method, expected_service_class
):
    result = getattr(async_account_users_service, service_method)("ACC-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"account_user_id": "ACC-0000-0001"}
