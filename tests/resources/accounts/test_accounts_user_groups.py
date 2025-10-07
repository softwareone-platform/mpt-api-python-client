import pytest

from mpt_api_client.resources.accounts.accounts_user_groups import (
    AccountsUserGroupsService,
    AsyncAccountsUserGroupsService,
)


@pytest.fixture
def accounts_user_groups_service(http_client):
    return AccountsUserGroupsService(
        http_client=http_client,
        endpoint_params={"account_id": "ACC-0000-0001", "user_id": "USR-0000-0001"},
    )


@pytest.fixture
def async_accounts_user_groups_service(async_http_client):
    return AsyncAccountsUserGroupsService(
        http_client=async_http_client,
        endpoint_params={"account_id": "ACC-0000-0001", "user_id": "USR-0000-0001"},
    )


def test_endpoint(accounts_user_groups_service):
    assert (
        accounts_user_groups_service.endpoint
        == "/public/v1/accounts/ACC-0000-0001/users/USR-0000-0001/groups"
    )


def test_async_endpoint(async_accounts_user_groups_service):
    assert (
        async_accounts_user_groups_service.endpoint
        == "/public/v1/accounts/ACC-0000-0001/users/USR-0000-0001/groups"
    )


@pytest.mark.parametrize(
    "method",
    ["create", "update", "delete"],
)
def test_mixins_present(accounts_user_groups_service, method):
    assert hasattr(accounts_user_groups_service, method)


@pytest.mark.parametrize(
    "method",
    ["create", "update", "delete"],
)
def test_async_mixins_present(async_accounts_user_groups_service, method):
    assert hasattr(async_accounts_user_groups_service, method)
