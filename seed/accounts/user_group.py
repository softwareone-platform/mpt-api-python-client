import logging

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.user_groups import UserGroup
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id

logger = logging.getLogger(__name__)


@inject
def build_user_group_data(
    context: Context = Provide[Container.context],
) -> dict[str, object]:
    """Get user group data dictionary for creation."""
    account_id = require_context_id(context, "accounts.client_account.id", "creating user group")
    module_id = require_context_id(context, "accounts.module.id", "creating user group")

    return {
        "name": "E2E Seeded User Group",
        "account": {"id": account_id},
        "buyers": None,
        "logo": "",
        "description": "User group for E2E tests",
        "modules": [{"id": module_id}],
    }


@inject
async def create_user_group(
    context: Context = Provide[Container.context],
    mpt_operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> UserGroup:
    """Creates a user group."""
    user_group_data = build_user_group_data(context=context)
    return await mpt_operations.accounts.user_groups.create(user_group_data)


async def seed_user_group() -> None:
    """Seed user group."""
    logger.debug("Seeding user group ...")
    await init_resource("accounts.user_group.id", create_user_group)
    logger.debug("Seeding user group completed.")
