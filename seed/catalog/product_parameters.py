import logging
from typing import Any

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.products_parameters import Parameter
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_VENDOR

logger = logging.getLogger(__name__)

namespace = "catalog.parameter"


@inject
async def get_parameter(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Parameter | None:
    """Get parameter from context or fetch from API."""
    parameter_id = context.get_string(f"{namespace}.id")
    if not parameter_id:
        return None
    try:
        return context.get_resource(namespace, parameter_id)  # type: ignore[return-value]
    except ValueError:
        logger.debug("Loading parameter: %s", parameter_id)
        product_id = context.get_string("catalog.product.id")
        parameter = await mpt_vendor.catalog.products.parameters(product_id).get(parameter_id)
        context.set_resource(namespace, parameter)
        return parameter


@inject
def build_parameter(context: Context = DEFAULT_CONTEXT) -> dict[str, Any]:
    """Build parameter data dictionary."""
    parameter_group_id = context.get_string("catalog.parameter_group.id")
    if not parameter_group_id:
        raise ValueError("Parameter group id is required.")
    return {
        "name": "Parameter Name",
        "scope": "Order",
        "phase": "Order",
        "description": "Agreement identifier of the reseller",
        "externalId": "RES-233-33-xx3",
        "displayOrder": 100,
        "context": "Purchase",
        "constraints": {"hidden": True, "readonly": True, "required": False},
        "type": "SingleLineText",
        "options": {
            "name": "Agreement Id",
            "placeholderText": "AGR-xxx-xxx-xxx",
            "hintText": "Add agreement id",
            "minChar": 15,
            "maxChar": 15,
            "defaultValue": None,
        },
        "group": {"id": parameter_group_id},
        "status": "active",
    }


@inject
async def create_parameter(
    context: Context = DEFAULT_CONTEXT, mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR
) -> Parameter:
    """Create parameter and stores it in the context."""
    product_id = context.get_string("catalog.product.id")
    if not product_id:
        raise ValueError("Product id is required.")
    parameter_data = build_parameter(context=context)
    parameter = await mpt_vendor.catalog.products.parameters(product_id).create(parameter_data)
    logger.debug("Parameter created: %s", parameter.id)
    context[f"{namespace}.id"] = parameter.id
    context.set_resource(namespace, parameter)
    return parameter


@inject
async def init_parameter(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Parameter:
    """Get or create parameter."""
    parameter = await get_parameter()

    if not parameter:
        logger.debug("Creating parameter ...")
        return await create_parameter(context, mpt_vendor)
    logger.debug("Parameter found: %s", parameter.id)
    return parameter


async def seed_parameters() -> None:
    """Seed catalog parameters."""
    logger.debug("Seeding catalog.parameter ...")
    await init_parameter()
    logger.debug("Seeded catalog.parameter completed.")
