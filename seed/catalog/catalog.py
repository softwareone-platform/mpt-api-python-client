import asyncio
import logging
from typing import Any

from seed.catalog.item import seed_items
from seed.catalog.item_group import seed_item_group
from seed.catalog.product import seed_product
from seed.catalog.product_parameters import seed_parameters
from seed.catalog.product_parameters_group import seed_parameter_group

logger = logging.getLogger(__name__)


async def seed_groups_and_group_params() -> None:
    """Seed parallel tasks for item groups and parameter groups."""
    tasks: list[asyncio.Task[Any]] = [
        asyncio.create_task(seed_item_group()),
        asyncio.create_task(seed_parameter_group()),
    ]
    await asyncio.gather(*tasks)


async def seed_items_and_params() -> None:
    """Seed final tasks for items and parameters."""
    tasks: list[asyncio.Task[Any]] = [
        asyncio.create_task(seed_items()),
        asyncio.create_task(seed_parameters()),
    ]
    await asyncio.gather(*tasks)


async def seed_catalog() -> None:
    """Seed catalog data including products, item groups, and parameters."""
    logger.debug("Seeding catalog ...")
    await seed_product()
    await seed_groups_and_group_params()
    await seed_items_and_params()

    logger.debug("Seeded catalog completed.")
