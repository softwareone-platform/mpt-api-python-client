# mypy: disable-error-code=unreachable
import logging
import uuid

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.sellers import Seller
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS

logger = logging.getLogger(__name__)


@inject
async def get_seller(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Seller | None:
    """Get seller from context or fetch from API."""
    seller_id = context.get_string("accounts.seller.id")
    if not seller_id:
        return None
    try:
        seller = context.get_resource("accounts.seller", seller_id)
    except ValueError:
        seller = None
    if not isinstance(seller, Seller):
        seller = await mpt_operations.accounts.sellers.get(seller_id)
        context.set_resource("accounts.seller", seller)
        context["accounts.seller.id"] = seller.id
        return seller
    return seller


@inject
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
async def init_seller(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Seller | None:
    """Get or create seller. Returns Seller if successful, None otherwise."""
    seller = await get_seller(context=context, mpt_operations=mpt_operations)
    if seller is None:
        logger.debug("Creating seller ...")
        seller_data = build_seller_data()
        created = await mpt_operations.accounts.sellers.create(seller_data)
        if isinstance(created, Seller):
            context.set_resource("accounts.seller", created)
            context["accounts.seller.id"] = created.id
            logger.info("Seller created: %s", created.id)
            return created
        logger.warning("Seller creation failed")
        return None
    logger.info("Seller already exists: %s", seller.id)
    return seller


@inject
async def seed_seller() -> None:
    """Seed seller."""
    logger.debug("Seeding seller ...")
    await init_seller()
    logger.debug("Seeding seller completed.")
