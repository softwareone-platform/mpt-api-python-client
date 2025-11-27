from unittest.mock import AsyncMock, patch

from seed.commerce.commerce import seed_commerce


async def test_seed_commerce() -> None:
    with (
        patch(
            "seed.commerce.commerce.seed_agreement", new_callable=AsyncMock
        ) as mock_seed_agreement,
    ):
        await seed_commerce()  # act

        mock_seed_agreement.assert_called_once()
