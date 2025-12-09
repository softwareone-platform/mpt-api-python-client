import logging

from seed.catalog.authorization import seed_authorization
from seed.catalog.listing import seed_listing
from seed.catalog.price_list import seed_price_list
from seed.catalog.product import seed_product

logger = logging.getLogger(__name__)


async def seed_catalog() -> None:
    """Seed catalog data including products, item groups, and parameters."""
    logger.debug("Seeding catalog ...")
    await seed_product()
    await seed_authorization()
    await seed_price_list()
    await seed_listing()

    logger.debug("Seeded catalog completed.")
