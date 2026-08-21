import pytest

from mpt_api_client.resources.accounts.account_users import (
    AccountUsersService,
    AsyncAccountUsersService,
)

ACCOUNT_USERS_PATH = "/public/v1/accounts/account-users"


@pytest.fixture
def account_users_service(http_client):
    return AccountUsersService(http_client=http_client)


@pytest.fixture
def async_account_users_service(async_http_client):
    return AsyncAccountUsersService(http_client=async_http_client)


def test_endpoint(account_users_service):
    result = account_users_service.build_path()

    assert result == ACCOUNT_USERS_PATH


def test_async_endpoint(async_account_users_service):
    result = async_account_users_service.build_path()

    assert result == ACCOUNT_USERS_PATH


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "accept_invite", "resend_invite", "send_new_invite"],
)
def test_methods_present(account_users_service, method):
    result = hasattr(account_users_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "accept_invite", "resend_invite", "send_new_invite"],
)
def test_async_methods_present(async_account_users_service, method):
    result = hasattr(async_account_users_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["update"])
def test_undocumented_methods_absent(account_users_service, method):
    result = hasattr(account_users_service, method)

    assert result is False


@pytest.mark.parametrize("method", ["update"])
def test_async_undocumented_methods_absent(async_account_users_service, method):
    result = hasattr(async_account_users_service, method)

    assert result is False
