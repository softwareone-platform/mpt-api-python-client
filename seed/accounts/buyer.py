import logging
import os
import pathlib

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.buyers import Buyer
from seed.container import Container
from seed.context import Context

logger = logging.getLogger(__name__)

icon = pathlib.Path(__file__).parent.parent / "data/logo.png"


@inject
async def get_buyer(
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Buyer | None:
    """
    Retrieve the buyer identified by "accounts.buyer.id" from the context or fetch it from the API and cache it.
    
    If the context does not contain "accounts.buyer.id", returns `None`. If the id exists but no valid Buyer instance is cached, fetches the buyer from the API, stores it in the context under "accounts.buyer", updates "accounts.buyer.id" with the fetched buyer's id, and returns the Buyer.
    
    Returns:
        Buyer or `None` if "accounts.buyer.id" is not set in the context.
    """
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
def build_buyer_data(context: Context = Provide[Container.context]) -> dict[str, object]:
    """
    Builds the payload dictionary used to create a buyer in the MPT API.
    
    Reads CLIENT_ACCOUNT_ID from the environment and `accounts.seller.id` from the provided context to populate required account and seller references.
    
    Parameters:
    	context (Context): Application context used to read `accounts.seller.id`.
    
    Returns:
    	dict[str, object]: Buyer data payload including name, account, sellers, contact, and address.
    
    Raises:
    	ValueError: If CLIENT_ACCOUNT_ID environment variable is missing.
    	ValueError: If `accounts.seller.id` is not found in the context.
    """
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
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Buyer:
    """
    Ensure a Buyer exists in the provided context, creating one via the API if none is present.
    
    Returns:
        Buyer: The existing or newly created Buyer instance.
    
    Raises:
        ValueError: If buyer creation via the API fails.
    """
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