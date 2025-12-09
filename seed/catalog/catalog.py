import logging

from seed.catalog.authorization import seed_authorization
from seed.catalog.listing import seed_listing
from seed.catalog.price_list import seed_price_list
from seed.catalog.product import seed_product

logger = logging.getLogger(__name__)


async def seed_catalog() -> None:
    """
    Seed catalog data in a defined sequence.
    
    Seeds products first, then authorization data, then price lists, and finally listings to ensure dependent catalog data is created in order.
    """
    logger.debug("Seeding catalog ...")
    await seed_product()
    await seed_authorization()
    await seed_price_list()
    await seed_listing()

    logger.debug("Seeded catalog completed.")