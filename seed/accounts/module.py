import logging

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.modules import Module
from mpt_api_client.rql.query_builder import RQLQuery
from seed.container import Container
from seed.context import Context

logger = logging.getLogger(__name__)


@inject
async def get_module(
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Module | None:
    """Get module from context or fetch from API."""
    module_id = context.get_string("accounts.module.id")
    if not module_id:
        return None
    try:
        module = context.get_resource("accounts.module", module_id)
    except ValueError:
        module = None
    if not isinstance(module, Module):
        module = await mpt_operations.accounts.modules.get(module_id)
        context.set_resource("accounts.module", module)
        context["accounts.module.id"] = module.id
        return module
    return module


@inject
async def refresh_module(
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Module | None:
    """Refresh module in context (always fetch)."""
    module = await get_module(context=context, mpt_operations=mpt_operations)
    if module is None:
        filtered_modules = mpt_operations.accounts.modules.filter(
            RQLQuery(name="Access Management")
        )
        modules = [mod async for mod in filtered_modules.iterate()]
        if modules:
            first_module = modules[0]
            if isinstance(first_module, Module):
                context["accounts.module.id"] = first_module.id
                context.set_resource("accounts.module", first_module)
                return first_module
            logger.warning("First module is not a Module instance.")
            return None
        logger.warning("Module 'Access Management' not found.")
        return None
    return module


@inject
async def seed_module() -> Module:
    """Seed module."""
    logger.debug("Seeding module ...")
    existing_module = await get_module()
    if existing_module is None:
        refreshed = await refresh_module()
        logger.debug("Seeding module completed.")
        if refreshed is None:
            raise ValueError("Could not seed module: no valid Module found.")
        return refreshed
    logger.debug("Seeding module completed.")
    return existing_module
