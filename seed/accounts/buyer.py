import logging
import pathlib

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.buyers import Buyer
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS

logger = logging.getLogger(__name__)

icon = pathlib.Path(__file__).parent / "logo.png"


@inject
async def get_buyer(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Buyer | None:
    """Get buyer from context or fetch from API."""
    buyer_id = context.get_string("accounts.buyer.id")
    logger.debug("Getting buyer: %s", buyer_id)
    if not buyer_id:
        return None
    try:
        buyer = context.get_resource("accounts.buyer", buyer_id)
    except ValueError:
        buyer = None
    if not isinstance(buyer, Buyer):
        logger.debug("Refreshing buyer: %s", buyer_id)
        buyer = await mpt_operations.accounts.buyers.get(buyer_id)
        context.set_resource("accounts.buyer", buyer)
        context["accounts.buyer.id"] = buyer.id
        return buyer
    return buyer


@inject
def build_buyer_data(context: Context = DEFAULT_CONTEXT):
    """Build buyer data dictionary for creation."""
    buyer_account_id = context.get_string("accounts.account.id")
    return {
            "name": "E2E Seeded Buyer",
            "account": {
                "id": buyer_account_id,
            },
            "contact": {
                "firstName": "first",
                "lastName": "last",
                "email": "created.buyer@example.com",
            },
            "address": {
                "addressLine1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "postCode": "12345",
                "country": "US",
            },
        }


@inject
async def init_buyer(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Buyer:
    """Get or create buyer."""
    buyer = await get_buyer()
    if buyer is None:
        buyer_data = build_buyer_data(context)
        logger.debug("Creating buyer ...")
        with pathlib.Path.open(icon, "rb") as icon_file:
            buyer = await mpt_operations.accounts.buyers.create(
                buyer_data, file=icon_file
            )
            context.set_resource("accounts.buyer", buyer)
            context["accounts.buyer.id"] = buyer.id
        logger.info("Buyer created: %s", buyer.id)
    else:
        logger.info("Buyer found: %s", buyer.id)
    return buyer


@inject
async def seed_buyer(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> None:
    """Seed buyer."""
    logger.debug("Seeding buyer ...")
    await init_buyer(context, mpt_operations)
    logger.debug("Seeding buyer completed.")
