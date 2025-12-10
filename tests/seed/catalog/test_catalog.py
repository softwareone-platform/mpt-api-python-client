from unittest.mock import patch

from seed.catalog.catalog import seed_catalog


async def test_seed_catalog() -> None:
    with (
        patch("seed.catalog.catalog.seed_product", autospec=True) as seed_product,
        patch("seed.catalog.catalog.seed_authorization", autospec=True) as seed_authorization,
        patch("seed.catalog.catalog.seed_price_list", autospec=True) as seed_price_list,
        patch("seed.catalog.catalog.seed_listing", autospec=True) as seed_listing,
    ):
        await seed_catalog()  # act

        seed_product.assert_awaited_once()
        seed_authorization.assert_awaited_once()
        seed_price_list.assert_awaited_once()
        seed_listing.assert_awaited_once()
