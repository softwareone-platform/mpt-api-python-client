from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.listings import Listing
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id


async def seed_listing() -> None:
    """Seed listing."""
    await init_resource("catalog.listing.id", create_listing)


@inject
async def create_listing(  # noqa: WPS210
    operations: AsyncMPTClient = Provide[Container.mpt_operations],
    context: Context = Provide[Container.context],
) -> Listing:
    """Creates a listing."""
    product_id = require_context_id(context, "catalog.product.id", "Create listing")
    seller_id = require_context_id(context, "accounts.seller.id", "Create listing")
    authorization_id = require_context_id(context, "catalog.authorization.id", "Create listing")
    account_id = require_context_id(context, "accounts.account.id", "Create listing")
    price_list_id = require_context_id(context, "catalog.price_list.id", "Create listing")

    listing_data = {
        "name": "e2e - please delete",
        "authorization": {
            "id": authorization_id,
        },
        "product": {
            "id": product_id,
        },
        "vendor": {
            "id": account_id,
        },
        "seller": {
            "id": seller_id,
        },
        "priceList": {"id": price_list_id},
        "primary": False,
        "notes": "",
        "eligibility": {"client": True, "partner": False},
    }
    return await operations.catalog.listings.create(listing_data)
