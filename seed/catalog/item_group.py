import logging
from typing import Any

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.products_item_groups import ItemGroup
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_VENDOR

logger = logging.getLogger(__name__)


@inject
async def get_item_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> ItemGroup | None:
    """Get item group from context or fetch from API."""
    item_group_id = context.get_string("catalog.item_group.id")
    if not item_group_id:
        return None
    try:
        item_group = context.get_resource("catalog.item_group", item_group_id)
    except ValueError:
        item_group = None
    if not isinstance(item_group, ItemGroup):
        logger.debug("Refreshing item group: %s", item_group_id)
        product_id = context.get_string("catalog.product.id")
        item_group = await mpt_vendor.catalog.products.item_groups(product_id).get(item_group_id)
        return set_item_group(item_group, context=context)
    return item_group


@inject
def set_item_group(
    item_group: ItemGroup,
    context: Context = DEFAULT_CONTEXT,
) -> ItemGroup:
    """Set item group in context."""
    context["catalog.item_group.id"] = item_group.id
    context.set_resource("catalog.item_group", item_group)
    return item_group


@inject
def build_item_group(context: Context = DEFAULT_CONTEXT) -> dict[str, Any]:
    """Build item group data dictionary."""
    product_id = context.get("catalog.product.id")
    return {
        "product": {"id": product_id},
        "name": "Items",
        "label": "Items",
        "description": "Default item group",
        "displayOrder": 100,
        "default": True,
        "multiple": True,
        "required": True,
    }


@inject
async def init_item_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> ItemGroup:
    """Get or create item group."""
    item_group = await get_item_group()

    if not item_group:
        logger.debug("Creating item group ...")
        product_id = context.get_string("catalog.product.id")
        item_group_data = build_item_group()
        item_group = await mpt_vendor.catalog.products.item_groups(product_id).create(
            item_group_data
        )
        logger.debug("Item group created: %s", item_group.id)
        return set_item_group(item_group)
    logger.debug("Item group found: %s", item_group.id)
    return item_group


async def seed_item_group() -> None:
    """Seed item group."""
    logger.debug("Seeding catalog.item_group ...")
    await init_item_group()
    logger.debug("Seeded catalog.item_group completed.")
