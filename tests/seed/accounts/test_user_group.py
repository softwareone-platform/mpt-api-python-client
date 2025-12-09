import pytest

from seed.accounts.user_group import (
    build_user_group_data,
    create_user_group,
    seed_user_group,
)
from seed.context import Context


@pytest.fixture
def context_with_data() -> Context:
    ctx = Context()
    ctx["accounts.client_account.id"] = "ACC-1111-1111"
    ctx["accounts.module.id"] = "MOD-456"
    return ctx


def test_build_user_group_data(context_with_data):
    expected_data = {
        "name": "E2E Seeded User Group",
        "account": {"id": "ACC-1111-1111"},
        "buyers": None,
        "logo": "",
        "description": "User group for E2E tests",
        "modules": [{"id": "MOD-456"}],
    }

    result = build_user_group_data(context=context_with_data)

    assert result == expected_data


async def test_create_user_group(mocker, operations_client, context_with_data):
    create_mock = mocker.AsyncMock(return_value={"id": "UGR-1111-1111"})
    operations_client.accounts.user_groups.create = create_mock

    result = await create_user_group(
        context=context_with_data,
        mpt_operations=operations_client,
    )

    assert result == {"id": "UGR-1111-1111"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["name"] == "E2E Seeded User Group"
    assert payload["account"]["id"] == "ACC-1111-1111"
    assert payload["modules"][0]["id"] == "MOD-456"


async def test_seed_user_group(mocker):
    mock_init_resource = mocker.patch(
        "seed.accounts.user_group.init_resource", new_callable=mocker.AsyncMock
    )

    await seed_user_group()

    mock_init_resource.assert_awaited_once()
