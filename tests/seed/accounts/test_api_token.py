import pytest

from seed.accounts.api_tokens import (
    build_api_token_data,
    create_api_token,
    seed_api_token,
)
from seed.context import Context


@pytest.fixture
def context_with_data() -> Context:
    ctx = Context()
    ctx["accounts.client_account.id"] = "client-acct-789"
    ctx["accounts.module.id"] = "mod-123"
    return ctx


def test_build_api_token_data(context_with_data):
    expected_data = {
        "account": {"id": "client-acct-789"},
        "name": "E2E Seeded API Token",
        "description": "This is a seeded API token for end-to-end testing.",
        "icon": "",
        "modules": [{"id": "mod-123"}],
    }

    result = build_api_token_data(context=context_with_data)

    assert result == expected_data


async def test_create_api_token(mocker, operations_client, context_with_data):
    create_mock = mocker.AsyncMock(return_value={"id": "api-token-1"})
    operations_client.accounts.api_tokens.create = create_mock

    result = await create_api_token(
        context=context_with_data,
        mpt_ops=operations_client,
    )

    assert result == {"id": "api-token-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["account"]["id"] == "client-acct-789"
    assert payload["modules"][0]["id"] == "mod-123"


async def test_seed_api_token(mocker):
    mock_init_resource = mocker.patch(
        "seed.accounts.api_tokens.init_resource", new_callable=mocker.AsyncMock
    )

    await seed_api_token()

    mock_init_resource.assert_called_once_with("accounts.api_token.id", create_api_token)
