from unittest.mock import AsyncMock, patch

from seed.catalog.catalog import seed_catalog, seed_groups_and_group_params, seed_items_and_params


async def test_seed_catalog_stage1() -> None:
    with (
        patch("seed.catalog.catalog.seed_item_group", new_callable=AsyncMock) as mock_item_group,
        patch(
            "seed.catalog.catalog.seed_parameter_group", new_callable=AsyncMock
        ) as mock_param_group,
    ):
        await seed_groups_and_group_params()

        mock_item_group.assert_called_once()
        mock_param_group.assert_called_once()


async def test_seed_catalog_stage2() -> None:
    with (
        patch("seed.catalog.catalog.seed_items", new_callable=AsyncMock) as mock_items,
        patch("seed.catalog.catalog.seed_parameters", new_callable=AsyncMock) as mock_params,
    ):
        await seed_items_and_params()

        mock_items.assert_called_once()
        mock_params.assert_called_once()


async def test_seed_catalog() -> None:
    with (
        patch("seed.catalog.catalog.seed_product", new_callable=AsyncMock) as mock_product,
        patch(
            "seed.catalog.catalog.seed_items_and_params", new_callable=AsyncMock
        ) as seed_items_and_params,
        patch(
            "seed.catalog.catalog.seed_groups_and_group_params", new_callable=AsyncMock
        ) as seed_groups_and_group_params,
    ):
        await seed_catalog()

        mock_product.assert_called_once()
        seed_items_and_params.assert_called_once()
        seed_groups_and_group_params.assert_called_once()
