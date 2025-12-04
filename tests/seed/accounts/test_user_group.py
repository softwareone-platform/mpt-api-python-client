import pytest

from mpt_api_client.resources.accounts.user_groups import AsyncUserGroupsService, UserGroup
from seed.accounts.user_group import (
    build_user_group_data,
    get_user_group,
    init_user_group,
    seed_user_group,
)
from seed.context import Context


@pytest.fixture
def user_group():
    return UserGroup({"id": "UG-123", "name": "Test User Group"})


@pytest.fixture
def user_groups_service(mocker):
    return mocker.Mock(spec=AsyncUserGroupsService)


async def test_get_user_group(context: Context, operations_client, user_group, user_groups_service):
    context["accounts.user_group.id"] = user_group.id
    user_groups_service.get.return_value = user_group
    operations_client.accounts.user_groups = user_groups_service

    result = await get_user_group(context=context, mpt_operations=operations_client)

    assert result == user_group
    assert context.get_resource("accounts.user_group", user_group.id) == user_group


async def test_get_user_group_without_id(context: Context):
    result = await get_user_group(context=context)
    assert result is None


async def test_init_user_group(  # noqa: WPS211
    context: Context, operations_client, user_groups_service, user_group, monkeypatch, mocker
):
    user_groups_service.create.return_value = user_group
    operations_client.accounts.user_groups = user_groups_service
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.module.id"] = "MOD-456"
    mocker.patch(
        "seed.accounts.user_group.get_user_group", new_callable=mocker.AsyncMock, return_value=None
    )
    mocker.patch(
        "seed.accounts.user_group.build_user_group_data",
        return_value=build_user_group_data(context),
    )
    result = await init_user_group(context=context, mpt_operations=operations_client)
    assert result == user_group
    user_groups_service.create.assert_called_once()


def test_build_user_group_data(context: Context, monkeypatch):
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.module.id"] = "MOD-456"
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


async def test_seed_user_group(mocker):
    mock_init_user_group = mocker.patch(
        "seed.accounts.user_group.init_user_group", new_callable=mocker.AsyncMock
    )
    await seed_user_group()  # act
    mock_init_user_group.assert_awaited_once()
