import logging
import uuid

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.sellers import Seller
from seed.container import Container
from seed.helper import init_resource

logger = logging.getLogger(__name__)


def build_seller_data(external_id: str | None = None) -> dict[str, object]:
    """Get seller data dictionary for creation."""
    if external_id is None:
        external_id = f"ext-{uuid.uuid4()}"
    return {
        "name": "E2E Seeded Seller",
        "address": {
            "addressLine1": "123 Main St",
            "city": "Los Angeles",
            "state": "CA",
            "postCode": "12345",
            "country": "US",
        },
        "currencies": ["USD", "EUR"],
        "externalId": external_id,  # Must be unique in Marketplace
    }


@inject
async def create_seller(
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Seller:
    """Creates a seller."""
    seller_data = build_seller_data()
    return await mpt_operations.accounts.sellers.create(seller_data)


async def seed_seller() -> None:
    """Seed seller."""
    logger.debug("Seeding seller ...")
    await init_resource("accounts.seller.id", create_seller)
    logger.debug("Seeding seller completed.")
