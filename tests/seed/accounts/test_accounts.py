from unittest.mock import AsyncMock, patch

from seed.accounts.accounts import seed_accounts


async def test_seed_accounts() -> None:
    with (
        patch("seed.accounts.accounts.seed_account", new_callable=AsyncMock) as mock_seed_account,
        patch("seed.accounts.accounts.seed_seller", new_callable=AsyncMock) as mock_seed_seller,
        patch("seed.accounts.accounts.seed_buyer", new_callable=AsyncMock) as mock_seed_buyer,
        patch("seed.accounts.accounts.seed_module", new_callable=AsyncMock) as mock_seed_module,
        patch(
            "seed.accounts.accounts.seed_api_token", new_callable=AsyncMock
        ) as mock_seed_api_token,
        patch(
            "seed.accounts.accounts.seed_user_group", new_callable=AsyncMock
        ) as mock_seed_user_group,
        patch("seed.accounts.accounts.seed_licensee", new_callable=AsyncMock) as mock_seed_licensee,
    ):
        await seed_accounts()  # act

        mocks = [
            mock_seed_account,
            mock_seed_seller,
            mock_seed_buyer,
            mock_seed_module,
            mock_seed_api_token,
            mock_seed_user_group,
            mock_seed_licensee,
        ]
        for mock in mocks:
            mock.assert_called_once()
