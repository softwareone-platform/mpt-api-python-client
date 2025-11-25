import io
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mpt_api_client.resources.accounts.account import Account, AsyncAccountsService
from seed.accounts.account import get_account, init_account, seed_account
from seed.context import Context


@pytest.fixture
def account():
    return Account({"id": "acc-123", "name": "Test Account"})


@pytest.fixture
def accounts_service():
    return AsyncMock(spec=AsyncAccountsService)


async def test_get_account(context: Context, operations_client, account, accounts_service) -> None:
    context["accounts.account.id"] = account.id
    accounts_service.get.return_value = account
    operations_client.accounts.accounts = accounts_service

    result = await get_account(context=context, mpt_operations=operations_client)

    assert result == account
    assert context.get_resource("accounts.account", account.id) == account


async def test_get_account_without_id(context: Context) -> None:
    result = await get_account(context=context)

    assert result is None


async def test_init_account_create_new(
    context: Context, operations_client, accounts_service, account
) -> None:
    accounts_service.create.return_value = account
    operations_client.accounts.accounts = accounts_service
    fake_icon_bytes = io.BytesIO(b"fake image")

    with (
        patch("seed.accounts.account.get_account", return_value=None),
        patch("seed.accounts.account.icon", new=MagicMock()),
        patch("pathlib.Path.open", return_value=fake_icon_bytes),
    ):
        result = await init_account(context, mpt_operations=operations_client)
        assert result == account
        accounts_service.create.assert_called_once()


async def test_seed_account() -> None:
    with (
        patch("seed.accounts.account.init_account", new_callable=AsyncMock) as mock_init_account,
    ):
        await seed_account()  # act
        mock_init_account.assert_awaited_once()
