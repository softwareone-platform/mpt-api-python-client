import io
from unittest.mock import AsyncMock, patch

import pytest

from mpt_api_client.resources.accounts.api_tokens import ApiToken, AsyncApiTokensService
from seed.accounts.api_tokens import (
    build_api_token_data,
    get_api_token,
    init_api_token,
    seed_api_token,
)
from seed.context import Context


@pytest.fixture
def api_token():
    return ApiToken({"id": "TOK-123", "name": "Test Token"})


@pytest.fixture
def api_tokens_service():
    return AsyncMock(spec=AsyncApiTokensService)


async def test_get_api_token(
    context: Context, operations_client, api_token, api_tokens_service
) -> None:
    context["accounts.api_token.id"] = api_token.id
    api_tokens_service.get.return_value = api_token
    operations_client.accounts.api_tokens = api_tokens_service

    result = await get_api_token(context=context, mpt_operations=operations_client)

    assert result == api_token
    assert context.get_resource("accounts.api_token", api_token.id) == api_token


async def test_get_api_token_without_id(context: Context) -> None:
    result = await get_api_token(context=context)
    assert result is None


async def test_init_api_token(
    context: Context, operations_client, api_tokens_service, api_token
) -> None:
    api_tokens_service.create.return_value = api_token
    operations_client.accounts.api_tokens = api_tokens_service

    result = await init_api_token(context, mpt_operations=operations_client)

    assert result == api_token
    api_tokens_service.create.assert_called_once()


def test_build_api_token_data(context: Context) -> None:
    context["accounts.account.id"] = "ACC-123"
    context["accounts.module.id"] = "MOD-456"
    expected_data = {
        "account": {"id": "ACC-123"},
        "name": "E2E Seeded API Token",
        "description": "This is a seeded API token for end-to-end testing.",
        "icon": "",
        "modules": [{"id": "MOD-456"}],
    }

    result = build_api_token_data(context)

    assert result == expected_data


async def test_init_api_token_create_new(
    context: Context, operations_client, api_tokens_service, api_token
) -> None:
    api_tokens_service.create.return_value = api_token
    operations_client.accounts.api_tokens = api_tokens_service

    with patch("seed.accounts.api_token.get_api_token", return_value=None):
        result = await init_api_token(context, mpt_operations=operations_client)
        assert result == api_token
        api_tokens_service.create.assert_called_once()


async def test_seed_api_token() -> None:
    with (
        patch(
            "seed.accounts.api_token.init_api_token", new_callable=AsyncMock
        ) as mock_init_api_token,
    ):
        await seed_api_token()  # act
        mock_init_api_token.assert_awaited_once()
