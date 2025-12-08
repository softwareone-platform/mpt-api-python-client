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
    """Refresh item in context (always fetch)."""
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
    """Get item from context or fetch from API if not cached."""
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
    """Build item data dictionary for creation."""
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
    """Create item and cache in context."""
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
    """Review item if in draft status and cache result."""
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
    """Publish item if in reviewing status and cache result."""
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
