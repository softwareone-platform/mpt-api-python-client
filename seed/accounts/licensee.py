import logging
import os
import pathlib

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.licensees import Licensee
from seed.container import Container
from seed.context import Context

logger = logging.getLogger(__name__)

icon = pathlib.Path("seed/data/logo.png").resolve()


@inject
async def get_licensee(
    context: Context = Provide[Container.context],
    mpt_client: AsyncMPTClient = Provide[Container.mpt_client],
) -> Licensee | None:
    """Get licensee from context or fetch from API."""
    licensee_id = context.get_string("accounts.licensee.id")
    if not licensee_id:
        return None
    try:
        licensee = context.get_resource("accounts.licensee", licensee_id)
    except ValueError:
        licensee = None
    if not isinstance(licensee, Licensee):
        licensee = await mpt_client.accounts.licensees.get(licensee_id)
        context.set_resource("accounts.licensee", licensee)
        context["accounts.licensee.id"] = licensee.id
        return licensee
    return licensee


@inject
def build_licensee_data(  # noqa: WPS238
    context: Context = Provide[Container.context],
) -> dict[str, object]:
    """Get licensee data dictionary for creation."""
    account_id = os.getenv("CLIENT_ACCOUNT_ID")
    if not account_id:
        raise ValueError("CLIENT_ACCOUNT_ID environment variable is required")
    seller_id = context.get_string("accounts.seller.id")
    if not seller_id:
        raise ValueError("Seller ID is required in context")
    buyer_id = context.get_string("accounts.buyer.id")
    if not buyer_id:
        raise ValueError("Buyer ID is required in context")
    group = context.get_resource("accounts.user_group")
    if group is None:
        raise ValueError("User group is required in context")
    licensee_type = "Client"
    return {
        "name": "E2E Seeded Licensee",
        "address": {
            "addressLine1": "123 Main St",
            "city": "Los Angeles",
            "state": "CA",
            "postCode": "67890",
            "country": "US",
        },
        "useBuyerAddress": False,
        "seller": {"id": seller_id},
        "buyer": {"id": buyer_id},
        "account": {"id": account_id},
        "eligibility": {"client": True, "partner": False},
        "groups": [{"id": group.id}],
        "type": licensee_type,
        "status": "Enabled",
        "defaultLanguage": "en-US",
    }


@inject
async def init_licensee(
    context: Context = Provide[Container.context],
    mpt_client: AsyncMPTClient = Provide[Container.mpt_client],
) -> Licensee:
    """Get or create licensee."""
    licensee = await get_licensee(context=context, mpt_client=mpt_client)
    if licensee is None:
        licensee_data = build_licensee_data(context=context)
        logger.debug("Creating licensee ...")
        with open(str(icon), "rb") as icon_file:  # noqa: PTH123
            created = await mpt_client.accounts.licensees.create(licensee_data, file=icon_file)
        if isinstance(created, Licensee):
            context.set_resource("accounts.licensee", created)
            context["accounts.licensee.id"] = created.id
            logger.info("Licensee created: %s", created.id)
            return created
        logger.warning("Licensee creation failed")
        raise ValueError("Licensee creation failed")
    logger.info("Licensee found: %s", licensee.id)
    return licensee


@inject
async def seed_licensee() -> None:
    """Seed licensee."""
    logger.debug("Seeding licensee ...")
    await init_licensee()
    logger.info("Seeding licensee completed.")
