import pytest

from mpt_api_client.resources.accounts.user_groups import (
    AsyncUserGroupsService,
    UserGroupsService,
)


@pytest.fixture
def user_groups_service(http_client):
    return UserGroupsService(http_client=http_client)


@pytest.fixture
def async_user_groups_service(http_client):
    return AsyncUserGroupsService(http_client=http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete"],
)
def test_mixins_present(user_groups_service, method):
    result = hasattr(user_groups_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete"],
)
def test_async_mixins_present(async_user_groups_service, method):
    result = hasattr(async_user_groups_service, method)

    assert result is True
