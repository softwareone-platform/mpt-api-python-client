import logging

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.buyers import Buyer
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id
from seed.static.static import ICON

logger = logging.getLogger(__name__)


def build_buyer_data(context: Context = Provide[Container.context]) -> dict[str, object]:
    """Build buyer data dictionary for creation."""
    buyer_account_id = require_context_id(context, "accounts.account.id", "creating buyer")
    seller_id = require_context_id(context, "accounts.seller.id", "creating buyer")
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
async def create_buyer(
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Buyer:
    """Creates a buyer."""
    buyer_data = build_buyer_data(context=context)
    with ICON.open("rb") as icon_fd:
        return await mpt_operations.accounts.buyers.create(buyer_data, file=icon_fd)


async def seed_buyer() -> None:
    """Seed buyer."""
    logger.debug("Seeding buyer ...")
    await init_resource("accounts.buyer.id", create_buyer)
    logger.debug("Seeding buyer completed.")
