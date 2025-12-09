from dependency_injector.wiring import Provide

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.price_lists import PriceList
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id


async def seed_price_list(context: Context = Provide[Container.context]) -> None:
    """
    Ensure a catalog price list resource exists, creating it if absent.
    
    Parameters:
        context (Context): Runtime context used to resolve and persist resource identifiers.
    """
    await init_resource("catalog.price_list.id", create_price_list, context)


async def create_price_list(
    operations: AsyncMPTClient = Provide[Container.mpt_operations],
    context: Context = Provide[Container.context],
) -> PriceList:
    """
    Create a price list for the product identified in the provided context.
    
    The function obtains the product id from `context` using the key "catalog.product.id" and sends a request to create a PriceList with seeded fields (notes, default markup, currency, and default flag).
    
    Returns:
        The created `PriceList` instance.
    """
    product_id = require_context_id(context, "catalog.product.id", "Create price list")

    price_list_data = {
        "notes": "E2E Seeded",
        "defaultMarkup": "20.0",
        "product": {"id": product_id},
        "currency": "USD",
        "default": False,
    }
    return await operations.catalog.price_lists.create(price_list_data)