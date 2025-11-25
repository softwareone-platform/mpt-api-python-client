import logging
import pathlib

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.licensees import Licensee
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_CLIENT

logger = logging.getLogger(__name__)

icon = pathlib.Path(__file__).parent / "logo.png"


@inject
async def get_licensee(
    context: Context = DEFAULT_CONTEXT,
    mpt_client: AsyncMPTClient = DEFAULT_MPT_CLIENT,
) -> Licensee | None:
    """Get licensee from context or fetch from API."""
    licensee_id = context.get_string("accounts.licensee.id")
    logger.debug("Getting licensee: %s", licensee_id)
    if not licensee_id:
        return None
    try:
        licensee = context.get_resource("accounts.licensee", licensee_id)
    except ValueError:
        licensee = None
    if not isinstance(licensee, Licensee):
        logger.debug("Refreshing licensee: %s", licensee_id)
        licensee = await mpt_client.accounts.licensees.get(licensee_id)
        context.set_resource("accounts.licensee", licensee)
        context["accounts.licensee.id"] = licensee.id
        return licensee
    return licensee


@inject
def build_licensee_data(
    context: Context = DEFAULT_CONTEXT,
) -> dict:
    """Get licensee data dictionary for creation."""
    account_id = context.get_string("accounts.account.id")
    seller_id = context.get_string("accounts.seller.id")
    buyer_id = context.get_string("accounts.buyer.id")
    group = context.get_resource("accounts.user_group")
    licensee_type = "Client"
    return {
        "name": "E2E Seeded Licensee",
        "address": {
            "addressLine1": "456 Licensee St",
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
        "groups": [group],
        "type": licensee_type,
        "status": "Enabled",
        "defaultLanguage": "en-US",
    }

@inject
async def init_licensee(
    context: Context = DEFAULT_CONTEXT,
    mpt_client: AsyncMPTClient = DEFAULT_MPT_CLIENT,
) -> Licensee:
    """Get or create licensee."""
    licensee = await get_licensee()
    if licensee is None:
        licensee_data = build_licensee_data(context)
        logger.debug("Creating licensee ...")
        with pathlib.Path.open(icon, "rb") as icon_file:
            licensee = await mpt_client.accounts.licensees.create(
                licensee_data, file=icon_file
            )
            context.set_resource("accounts.licensee", licensee)
            context["accounts.licensee.id"] = licensee.id
        logger.info("Licensee created: %s", licensee.id)
    else:
        logger.info("Licensee found: %s", licensee.id)
    return licensee


@inject
async def seed_licensee(
    context: Context = DEFAULT_CONTEXT,
    mpt_client: AsyncMPTClient = DEFAULT_MPT_CLIENT,
) -> None:
    """Seed licensee."""
    logger.debug("Seeding licensee ...")
    await init_licensee(context, mpt_client)
    logger.info("Seeding licensee completed.")
