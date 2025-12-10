import pytest

from mpt_api_client.resources.accounts.api_tokens import ApiToken
from seed.accounts.api_tokens import (
    build_api_token_data,
    create_api_token,
    seed_api_token,
)


@pytest.fixture
def api_token():
    return ApiToken({"id": "TOK-123", "name": "Test Token"})


def test_build_api_token_data(context, monkeypatch):
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-1086-6867")
    context["accounts.module.id"] = "MOD-456"
    context["accounts.account.id"] = "ACC-1086-6867"
    expected_data = {
        "account": {"id": "ACC-1086-6867"},
        "name": "E2E Seeded API Token",
        "description": "This is a seeded API token for end-to-end testing.",
        "icon": "",
        "modules": [{"id": "MOD-456"}],
    }

    result = build_api_token_data(context=context)

    assert result == expected_data


async def test_create_api_token(mocker, api_token, operations_client):
    create = mocker.AsyncMock(return_value=api_token)
    operations_client.accounts.api_tokens.create = create
    build_api_token_data = mocker.patch(
        "seed.accounts.api_tokens.build_api_token_data", autospec=True
    )

    result = await create_api_token(operations_client)

    assert result == api_token
    build_api_token_data.assert_called_once()
    create.assert_awaited_once()


async def test_seed_api_token(mocker):
    init_resource = mocker.patch("seed.accounts.api_tokens.init_resource", autospec=True)
    await seed_api_token()  # act
    init_resource.assert_awaited_once()
