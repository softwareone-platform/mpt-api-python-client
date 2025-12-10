import pytest

from mpt_api_client.resources.accounts.account import Account
from seed.accounts.accounts import get_account, seed_accounts


async def test_get_account_fails(monkeypatch):
    # when env var is missing -> raises
    monkeypatch.delenv("CLIENT_ACCOUNT_ID", raising=False)
    with pytest.raises(ValueError):
        await get_account()


async def test_get_account_success(monkeypatch):
    # when env var is present -> returns Account with same id
    monkeypatch.setenv("CLIENT_ACCOUNT_ID", "ACC-123")
    account = await get_account()
    assert isinstance(account, Account)
    assert account.id == "ACC-123"


async def test_seed_accounts(mocker):  # noqa: WPS210
    mock_init_resource = mocker.patch("seed.accounts.accounts.init_resource", autospec=True)

    mock_seed_seller = mocker.patch("seed.accounts.accounts.seed_seller", autospec=True)
    mock_seed_buyer = mocker.patch("seed.accounts.accounts.seed_buyer", autospec=True)
    mock_seed_module = mocker.patch("seed.accounts.accounts.seed_module", autospec=True)
    mock_seed_api_token = mocker.patch("seed.accounts.accounts.seed_api_token", autospec=True)
    mock_seed_user_group = mocker.patch("seed.accounts.accounts.seed_user_group", autospec=True)
    mock_seed_licensee = mocker.patch("seed.accounts.accounts.seed_licensee", autospec=True)
    await seed_accounts()  # act
    mocks = [
        mock_seed_seller,
        mock_seed_buyer,
        mock_seed_module,
        mock_seed_api_token,
        mock_seed_user_group,
        mock_seed_licensee,
        mock_init_resource,
    ]
    for mock in mocks:
        mock.assert_awaited_once()
