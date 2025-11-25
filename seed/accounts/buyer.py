import logging
import os
import pathlib

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.buyers import Buyer
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS

logger = logging.getLogger(__name__)

icon = pathlib.Path("seed/data/logo.png").resolve()


@inject
async def get_buyer(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Buyer | None:
    """Get buyer from context or fetch from API."""
    buyer_id = context.get_string("accounts.buyer.id")
    if not buyer_id:
        return None
    try:
        buyer = context.get_resource("accounts.buyer", buyer_id)
    except ValueError:
        buyer = None
    if not isinstance(buyer, Buyer):
        buyer = await mpt_operations.accounts.buyers.get(buyer_id)
        context.set_resource("accounts.buyer", buyer)
        context["accounts.buyer.id"] = buyer.id
        return buyer
    return buyer


@inject
def build_buyer_data(context: Context = DEFAULT_CONTEXT) -> dict[str, object]:
    """Build buyer data dictionary for creation."""
    buyer_account_id = os.getenv("CLIENT_ACCOUNT_ID")
    if not buyer_account_id:
        raise ValueError("CLIENT_ACCOUNT_ID environment variable is required")
    seller_id = context.get_string("accounts.seller.id")
    if not seller_id:
        raise ValueError("accounts.seller.id missing from context; seed seller before buyer.")
    return {
        "name": "E2E Seeded Buyer",
        "account": {"id": buyer_account_id},
        "sellers": [{"id": seller_id}],
        "contact": {
            "firstName": "first",
            "lastName": "last",
            "email": "created.buyer@example.com",
        },
        "address": {
            "addressLine1": "123 Main St",
            "city": "Los Angeles",
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
    buyer = await get_buyer(context=context, mpt_operations=mpt_operations)
    if buyer is None:
        buyer_data = build_buyer_data(context=context)
        logger.debug("Creating buyer ...")
        with open(str(icon), "rb") as icon_file:  # noqa: PTH123
            created = await mpt_operations.accounts.buyers.create(buyer_data, file=icon_file)
        if isinstance(created, Buyer):
            context.set_resource("accounts.buyer", created)
            context["accounts.buyer.id"] = created.id
            logger.info("Buyer created: %s", created.id)
            return created
        logger.warning("Buyer creation failed")
        raise ValueError("Buyer creation failed")
    logger.info("Buyer found: %s", buyer.id)
    return buyer


@inject
async def seed_buyer() -> None:
    """Seed buyer."""
    logger.debug("Seeding buyer ...")
    await init_buyer()
    logger.debug("Seeding buyer completed.")
