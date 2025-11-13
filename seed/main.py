import asyncio
import logging

from seed.container import wire_container
from seed.seed_api import seed_api

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for seeding."""
    wire_container()
    await seed_api()


if __name__ == "__main__":
    asyncio.run(main())
