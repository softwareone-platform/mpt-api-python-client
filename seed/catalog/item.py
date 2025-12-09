import logging
from typing import Any

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.items import Item
from seed.container import Container
from seed.context import Context

logger = logging.getLogger(__name__)


@inject
async def refresh_item(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Item | None:
    """
    Fetch the catalog item from the vendor API and store it in the context.
    
    If the context does not contain a catalog item id under "catalog.item.id", no fetch is performed and the function returns `None`. When an item is fetched, its id is written back to "catalog.item.id" and the item resource is cached under "catalog.item" in the context.
    
    Returns:
        Item | None: The fetched `Item` cached in the context, or `None` if no item id was present.
    """
    item_id = context.get_string("catalog.item.id")
    if not item_id:
        return None
    item_resource = await mpt_vendor.catalog.items.get(item_id)
    context["catalog.item.id"] = item_resource.id
    context.set_resource("catalog.item", item_resource)
    return item_resource


@inject
async def get_item(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Item | None:
    """
    Retrieve the catalog item from the context cache or fetch it from the API and cache it if not present or invalid.
    
    Returns:
        Item if found in context or successfully fetched and cached, `None` if the context does not contain a catalog item id.
    """
    item_id = context.get_string("catalog.item.id")
    if not item_id:
        return None
    try:
        catalog_item = context.get_resource("catalog.item", item_id)
    except ValueError:
        catalog_item = None
    if not isinstance(catalog_item, Item):
        logger.debug("Loading item: %s", item_id)
        catalog_item = await mpt_vendor.catalog.items.get(item_id)
        context["catalog.item.id"] = catalog_item.id
        context.set_resource("catalog.item", catalog_item)
        return catalog_item
    return catalog_item


@inject
def build_item(context: Context = Provide[Container.context]) -> dict[str, Any]:
    """
    Builds a payload dictionary for creating a catalog item.
    
    Reads "catalog.product.id" and "catalog.item_group.id" from the provided context to populate the product and group references used in the payload.
    
    Parameters:
        context (Context): Context used to retrieve "catalog.product.id" and "catalog.item_group.id".
    
    Returns:
        dict[str, Any]: A dictionary suitable as a create-item request payload containing product and group references, parameters, name, description, unit, terms, quantityNotApplicable flag, and externalIds.
    """
    product_id = context.get("catalog.product.id")
    item_group_id = context.get("catalog.item_group.id")
    return {
        "product": {"id": product_id},
        "parameters": [],
        "name": "Product Item 1",
        "description": "Product Item 1 - Description",
        "group": {"id": item_group_id},
        "unit": {
            "id": "UNT-1229",
            "name": "<string> 1",
            "revision": 1,
            "description": "<string>TEST",
            "statistics": {"itemCount": 34},
        },
        "terms": {"model": "quantity", "period": "1m", "commitment": "1m"},
        "quantityNotApplicable": False,
        "externalIds": {"vendor": "item_1"},
    }


@inject
async def create_item(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Item:
    """
    Create a catalog item from context data and cache it in the context.
    
    Builds the item payload from values stored in the context, creates the item via the vendor API, stores the new item's id and resource in the context, and returns the created item.
    
    Returns:
        The created Item.
    """
    item_data = build_item(context=context)
    catalog_item = await mpt_vendor.catalog.items.create(item_data)
    context["catalog.item.id"] = catalog_item.id
    context.set_resource("catalog.item", catalog_item)
    return catalog_item


@inject
async def review_item(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Item | None:
    """
    Review the cached catalog item if its status is `Draft` and cache the updated item.
    
    Returns:
        The cached or updated `Item`, or `None` if no catalog item is present.
    """
    logger.debug("Reviewing catalog.item ...")
    catalog_item = context.get_resource("catalog.item")
    if catalog_item.status != "Draft":
        return catalog_item  # type: ignore[return-value]
    catalog_item = await mpt_vendor.catalog.items.review(catalog_item.id)
    context.set_resource("catalog.item", catalog_item)
    return catalog_item


@inject
async def publish_item(
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Item | None:
    """
    Publish the catalog item when its status is Reviewing and update the context cache.
    
    Returns:
        The published Item if a publish occurred, the unchanged cached Item if it was not in Reviewing status, or `None` if no catalog item existed in the context.
    """
    logger.debug("Publishing catalog.item ...")
    catalog_item = context.get_resource("catalog.item")
    if catalog_item.status != "Reviewing":
        return catalog_item  # type: ignore[return-value]
    catalog_item = await mpt_operations.catalog.items.publish(catalog_item.id)
    context.set_resource("catalog.item", catalog_item)
    return catalog_item


@inject
async def seed_items(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> None:
    """Seed catalog items (create/review/publish)."""
    logger.debug("Seeding catalog.item ...")
    existing = await refresh_item(context=context, mpt_vendor=mpt_vendor)
    if not existing:
        await create_item(context=context, mpt_vendor=mpt_vendor)
    await review_item(context=context, mpt_vendor=mpt_vendor)
    await publish_item(context=context, mpt_operations=mpt_operations)
    logger.debug("Seeded catalog.item completed.")