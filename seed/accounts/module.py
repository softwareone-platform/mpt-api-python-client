import logging

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.modules import Module
from mpt_api_client.rql.query_builder import RQLQuery
from seed.container import Container
from seed.helper import init_resource

logger = logging.getLogger(__name__)


@inject
async def find_module(
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> Module:
    """Selects an existing module to use for seeding purposes.

    Currently selects the "Access Management" module from the marketplace.
    """
    filtered = mpt_operations.accounts.modules.filter(RQLQuery(name="Access Management"))
    modules = [module async for module in filtered.iterate()]

    if not modules:
        raise ValueError("Module 'Access Management' not found.")
    return modules[0]


async def seed_module() -> None:
    """Seed module."""
    logger.debug("Seeding module ...")
    await init_resource("accounts.module.id", find_module)
    logger.debug("Seeding module completed.")
