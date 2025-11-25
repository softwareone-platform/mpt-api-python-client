import logging
import pathlib

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.user_groups import UserGroup
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS

logger = logging.getLogger(__name__)


@inject
async def get_user_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> UserGroup | None:
    """Get user group from context or fetch from API."""
    user_group_id = context.get_string("accounts.user_group.id")
    logger.debug("Getting user group: %s", user_group_id)
    if not user_group_id:
        return None
    try:
        user_group = context.get_resource("accounts.user_group", user_group_id)
    except ValueError:
        user_group = None
    if not isinstance(user_group, UserGroup):
        logger.debug("Refreshing user group: %s", user_group_id)
        user_group = await mpt_operations.accounts.user_groups.get(user_group_id)
        context.set_resource("accounts.user_group", user_group)
        context["accounts.user_group.id"] = user_group.id
        return user_group
    return user_group


@inject
def build_user_group_data(
    context: Context = DEFAULT_CONTEXT,
) -> dict:
    """Get user group data dictionary for creation."""
    account_id = context.get_string("accounts.account.id")
    module_id = context.get_string("accounts.module.id")
    return {
        "name": "E2E Seeded User Group",
        "account": {"id": account_id},
        "buyers": None,
        "logo": "",
        "description": "User group for E2E tests",
        "modules": [{"id": module_id}],
    }


@inject
async def init_user_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> UserGroup:
    """Get or create user group."""
    user_group = await get_user_group()
    if user_group is None:
        logger.debug("Creating user group ...")
        user_group_data = build_user_group_data()
        user_group = await mpt_operations.accounts.user_groups.create(user_group_data)
        context.set_resource("accounts.user_group", user_group)
        context["accounts.user_group.id"] = user_group.id
    else:
        logger.info("User group already exists: %s", user_group.id)
    return user_group

@inject
async def seed_user_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> UserGroup:
    """Seed user group."""
    logger.debug("Seeding user group ...")
    await init_user_group(context, mpt_operations)
    logger.debug("Seeding user group completed.")
