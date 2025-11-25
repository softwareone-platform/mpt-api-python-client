import logging

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.modules import Module
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS

logger = logging.getLogger(__name__)


@inject
async def get_module(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
):
    """Get module from context or fetch from API."""
    module_id = context.get_string("accounts.module.id")
    logger.debug("Getting module: %s", module_id)
    if not module_id:
        return None
    try:
        module = context.get_resource("accounts.module", module_id)
    except ValueError:
        module = None
    if not isinstance(module, Module):
        logger.debug("Refreshing module: %s", module_id)
        module = await mpt_operations.accounts.modules.get(module_id)
        context.set_resource("accounts.module", module)
        context["accounts.module.id"] = module.id
        return module
    return module


@inject
async def refresh_module(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Module | None:
    """Refresh module in context (always fetch)."""
    module = await get_module(context, mpt_operations)
    if module is None:
        limit = 10
        module = await mpt_operations.accounts.modules.fetch_page(limit=limit)[0]
        context["accounts.module.id"] = module.id
        context.set_resource("accounts.module", module)
    return module


@inject
async def seed_module(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Module:
    """Seed module."""
    logger.debug("Seeding module ...")
    existing_module = await get_module(context, mpt_operations)
    if existing_module is None:
        await refresh_module(context, mpt_operations)
    logger.debug("Seeding module completed.")
