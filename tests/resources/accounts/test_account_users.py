import pytest

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
    assert hasattr(account_users_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "accept_invite", "resend_invite", "send_new_invite"],
)
def test_async_methods_present(async_account_users_service, method):
    assert hasattr(async_account_users_service, method)
