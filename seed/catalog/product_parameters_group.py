import logging
from typing import Any

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.products_parameter_groups import ParameterGroup
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_VENDOR

logger = logging.getLogger(__name__)

namespace = "catalog.product.parameter_group"


@inject
async def get_parameter_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> ParameterGroup | None:
    """Get parameter group from context or fetch from API."""
    parameter_group_id = context.get_string(f"{namespace}.id")
    if not parameter_group_id:
        return None
    try:
        return context.get_resource(namespace, parameter_group_id)  # type: ignore[return-value]
    except ValueError:
        logger.debug("Loading parameter group: %s", parameter_group_id)
        product_id = context.get_string("catalog.product.id")
        parameter_group = await mpt_vendor.catalog.products.parameter_groups(product_id).get(
            parameter_group_id
        )
        context[f"{namespace}.id"] = parameter_group.id
        context.set_resource(namespace, parameter_group)
        return parameter_group


@inject
def build_parameter_group(context: Context = DEFAULT_CONTEXT) -> dict[str, Any]:
    """Build parameter group data dictionary."""
    return {
        "name": "e2e - seed",
        "label": "Parameter group label",
        "displayOrder": 100,
    }


@inject
async def init_parameter_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> ParameterGroup:
    """Get or create parameter group."""
    parameter_group = await get_parameter_group()

    if not parameter_group:
        return await create_parameter_group(context, mpt_vendor)
    logger.debug("Parameter group found: %s", parameter_group.id)
    return parameter_group


async def create_parameter_group(context: Context, mpt_vendor: AsyncMPTClient) -> ParameterGroup:
    """Create parameter group."""
    logger.debug("Creating parameter group ...")
    product_id = context.get_string("catalog.product.id")
    if not product_id:
        raise ValueError("Product id is required.")
    parameter_group_data = build_parameter_group()
    parameter_group = await mpt_vendor.catalog.products.parameter_groups(product_id).create(
        parameter_group_data
    )
    logger.debug("Parameter group created: %s", parameter_group.id)
    context[f"{namespace}.id"] = parameter_group.id
    context.set_resource(namespace, parameter_group)
    return parameter_group


async def seed_parameter_group() -> None:
    """Seed parameter group."""
    logger.debug("Seeding %s ...", namespace)
    await init_parameter_group()
    logger.debug("Seeded %s completed.", namespace)
