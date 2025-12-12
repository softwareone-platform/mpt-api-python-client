import pytest

from mpt_api_client.resources.accounts.user_groups import UserGroup
from seed.accounts.user_group import (
    build_user_group_data,
    create_user_group,
    seed_user_group,
)
from seed.context import Context


@pytest.fixture
def user_group():
    return UserGroup({"id": "UG-123", "name": "Test User Group"})


def test_build_user_group_data(context: Context, monkeypatch):
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.module.id"] = "MOD-456"
    context["accounts.account.id"] = "ACC-1086-6867"
    expected_data = {
        "name": "E2E Seeded User Group",
        "account": {"id": "ACC-1086-6867"},
        "buyers": None,
        "logo": "",
        "description": "User group for E2E tests",
        "modules": [{"id": "MOD-456"}],
    }

    result = build_user_group_data(context)

    assert result == expected_data


async def test_create_user_group(mocker, operations_client, user_group):
    create_mock = mocker.AsyncMock(return_value=user_group)
    operations_client.accounts.user_groups.create = create_mock
    mocker.patch("seed.accounts.user_group.build_user_group_data")

    result = await create_user_group(operations_client)

    assert result == user_group
    create_mock.assert_awaited_once()


async def test_seed_user_group(mocker):
    init_resource = mocker.patch("seed.accounts.user_group.init_resource", autospec=True)

    await seed_user_group()  # act

    init_resource.assert_awaited_once_with("accounts.user_group.id", create_user_group)
