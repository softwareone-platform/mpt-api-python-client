import pytest

from mpt_api_client.resources.accounts.account_user_groups import (
    AccountUserGroupsService,
    AsyncAccountUserGroupsService,
)


@pytest.fixture
def account_user_groups_service(http_client):
    return AccountUserGroupsService(
        http_client=http_client,
        endpoint_params={"account_user_id": "ACC-0000-0001"},
    )


@pytest.fixture
def async_account_user_groups_service(async_http_client):
    return AsyncAccountUserGroupsService(
        http_client=async_http_client,
        endpoint_params={"account_user_id": "ACC-0000-0001"},
    )


def test_endpoint(account_user_groups_service):
    result = account_user_groups_service.path == (
        "/public/v1/accounts/account-users/ACC-0000-0001/groups"
    )

    assert result is True


def test_async_endpoint(async_account_user_groups_service):
    result = async_account_user_groups_service.path == (
        "/public/v1/accounts/account-users/ACC-0000-0001/groups"
    )

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["create", "update", "delete"],
)
def test_mixins_present(account_user_groups_service, method):
    result = hasattr(account_user_groups_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["create", "update", "delete"],
)
def test_async_mixins_present(async_account_user_groups_service, method):
    result = hasattr(async_account_user_groups_service, method)

    assert result is True
