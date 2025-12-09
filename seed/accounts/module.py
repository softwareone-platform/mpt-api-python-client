import logging

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.modules import Module
from mpt_api_client.rql.query_builder import RQLQuery
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource

logger = logging.getLogger(__name__)


@inject
async def refresh_module(
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Module | None:
    """Refresh module in context (always fetch)."""
    module = None
    filtered_modules = mpt_operations.accounts.modules.filter(RQLQuery(name="Access Management"))
    modules = [mod async for mod in filtered_modules.iterate()]
    if modules:
        first_module = modules[0]
        if isinstance(first_module, Module):
            context["accounts.module.id"] = first_module.id
            module = first_module
        logger.warning("First module is not a Module instance.")
    logger.warning("Module 'Access Management' not found.")
    return module


async def seed_module() -> None:
    """Seed module."""
    logger.debug("Seeding module ...")
    await init_resource("accounts.module.id", refresh_module)
    logger.debug("Seeding module completed.")
