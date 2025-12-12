import logging

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.licensees import Licensee
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id
from seed.static.static import ICON

logger = logging.getLogger(__name__)


@inject
def build_licensee_data(  # noqa: WPS238
    context: Context = Provide[Container.context],
) -> dict[str, object]:
    """Get licensee data dictionary for creation."""
    account_id = require_context_id(context, "accounts.account.id", "creating licensee")
    seller_id = require_context_id(context, "accounts.seller.id", "create licensee")
    buyer_id = require_context_id(context, "accounts.buyer.id", "create licensee")
    user_group_id = require_context_id(context, "accounts.user_group.id", "create licensee")

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
        "groups": [{"id": user_group_id}],
        "type": licensee_type,
        "status": "Enabled",
        "defaultLanguage": "en-US",
    }


@inject
async def create_licensee(mpt_client: AsyncMPTClient = Provide[Container.mpt_client]) -> Licensee:
    """Create licensee."""
    licensee_data = build_licensee_data()
    with ICON.open("rb") as icon_fd:
        return await mpt_client.accounts.licensees.create(licensee_data, file=icon_fd)


async def seed_licensee() -> None:
    """Seed licensee."""
    logger.debug("Seeding licensee ...")
    await init_resource("accounts.licensee.id", create_licensee)
    logger.info("Seeding licensee completed.")
