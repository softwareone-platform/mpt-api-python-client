from unittest.mock import AsyncMock, patch

from seed.catalog.catalog import seed_catalog


async def test_seed_catalog() -> None:
    with (
        patch("seed.catalog.catalog.seed_product", new_callable=AsyncMock) as seed_product,
        patch(
            "seed.catalog.catalog.seed_authorization", new_callable=AsyncMock
        ) as seed_authorization,
        patch("seed.catalog.catalog.seed_price_list", new_callable=AsyncMock) as seed_price_list,
        patch("seed.catalog.catalog.seed_listing", new_callable=AsyncMock) as seed_listing,
    ):
        await seed_catalog()  # act

        seed_product.assert_called_once()
        seed_authorization.assert_called_once()
        seed_price_list.assert_called_once()
        seed_listing.assert_called_once()
