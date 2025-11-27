import asyncio
import logging
from typing import Any

from seed.commerce.agreement import seed_agreement

logger = logging.getLogger(__name__)


async def seed_commerce() -> None:
    """Seed commerce data including agreements."""
    logger.debug("Seeding commerce ...")
    await seed_agreement()
    logger.debug("Seeded commerce completed.")
